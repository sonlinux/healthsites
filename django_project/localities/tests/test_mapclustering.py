# -*- coding: utf-8 -*-
from django.test import TestCase


from .model_factories import LocalityF

from ..map_clustering import within_bbox, cluster, overlapping_area


class TestMapClustering(TestCase):
    def test_within_bbox(self):

        bbox = (0, 0, 180, 90)

        self.assertTrue(within_bbox(bbox, 10, 10))
        self.assertFalse(within_bbox(bbox, -10, 10))
        self.assertFalse(within_bbox(bbox, 10, 99))

    def test_overlapping_area(self):

        self.assertEqual(
            overlapping_area(zoom=0, pix_x=10, pix_y=10, lat=0),
            (14.0625, 14.0625)
        )

        self.assertEqual(
            overlapping_area(zoom=3, pix_x=10, pix_y=10, lat=45),
            (1.2429611388044781, 1.2429611388044781)
        )

        self.assertEqual(
            overlapping_area(zoom=6, pix_x=10, pix_y=10, lat=60),
            (0.10986328125000001, 0.10986328125000001)
        )

    def test_cluster(self):

        LocalityF.create(id=1)
        LocalityF.create(id=2)
        LocalityF.create(id=3)
        LocalityF.create(id=4)
        LocalityF.create(id=5)

        LocalityF.create(id=6, geom='POINT(30 30)')
        LocalityF.create(id=7, geom='POINT(32 32)')

        LocalityF.create(id=8, geom='POINT(45 45)')

        dict_cluster = cluster(3, 40, 40)

        self.assertListEqual(dict_cluster, [
            {'count': 5, 'geom': (0.0, 0.0), 'id': 1,
                'bbox': (-4.6875, -4.6875, 4.6875, 4.6875)},
            {'count': 2, 'geom': (30.0, 30.0), 'id': 6,
                'bbox': (
                    25.940505919760444, 25.940505919760444,
                    34.05949408023956, 34.05949408023956)},
            {'count': 1, 'geom': (45.0, 45.0), 'id': 8,
                'bbox': (
                    41.68543696318806, 41.68543696318806,
                    48.31456303681194, 48.31456303681194)}
            ])
