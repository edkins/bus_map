package io.pantheist.torontobusmap;

import org.apache.commons.csv.CSVRecord;

import java.util.Map;

/**
 * Created by giles on 23/09/17.
 */

public class MapDataShape {
    public final int shape_id;

    public final float shape_pt_lat;

    public final float shape_pt_lon;

    public final int shape_pt_sequence;

    public final float shape_dist_traveled;

    public MapDataShape(CSVRecord record) {
        shape_id = Integer.parseInt(record.get("shape_id"));
        shape_pt_lat = Float.parseFloat(record.get("shape_pt_lat"));
        shape_pt_lon = Float.parseFloat(record.get("shape_pt_lon"));
        shape_pt_sequence = Integer.parseInt(record.get("shape_pt_sequence"));
        shape_dist_traveled = Float.parseFloat(record.get("shape_dist_traveled"));
    }
}
