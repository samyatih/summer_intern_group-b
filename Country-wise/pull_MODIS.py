import os
import time
import ee
import pandas as pd


def initialize_earth_engine():
    try:
        ee.Initialize()
    except Exception:
        ee.Authenticate()
        ee.Initialize()


def export_one_image(image, folder, name, region, scale, crs):
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=name,
        folder=folder,
        fileNamePrefix=name,
        region=region,
        scale=scale,
        crs=crs,
        maxPixels=1e13,
    )
    task.start()

    while task.status()['state'] == 'RUNNING':
        print(f'Running export for {name}')
        time.sleep(10)

    print('Done.', task.status())
    return task


def append_band(current, previous):
    previous = ee.Image(previous) if previous is not None else None
    current = ee.Image(current).select([0, 1, 2, 3, 4, 5, 6])
    if previous is None:
        return current
    return previous.addBands(current)


def build_region(lon, lat, offset=0.11):
    return [
        [lon - offset, lat - offset],
        [lon - offset, lat + offset],
        [lon + offset, lat + offset],
        [lon + offset, lat - offset],
        [lon - offset, lat - offset],
    ]


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'locations_final.csv')

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f'Could not find locations file: {csv_path}')

    initialize_earth_engine()

    locations = pd.read_csv(csv_path)

    if locations.shape[1] < 4:
        raise ValueError('The locations CSV must contain at least four columns: loc1, loc2, lat, lon')

    img_coll = ee.ImageCollection('MODIS/MOD09A1').filterBounds(
        ee.Geometry.Rectangle([-106.5, 23, -64, 50])
    )
    img = img_coll.iterate(append_band, None)

    for row in locations.itertuples(index=False, name=None):
        if len(row) < 4:
            continue

        loc1, loc2, lat, lon = row[0], row[1], row[2], row[3]
        fname = f'{int(loc1)}_{int(loc2)}'

        region = build_region(float(lon), float(lat), offset=0.11)

        try:
            export_one_image(img, 'Data', fname, region, 500, 'EPSG:4326')
        except Exception as exc:
            print(f'Retry needed for {fname}: {exc}')
            time.sleep(10)
