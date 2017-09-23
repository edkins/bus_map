package io.pantheist.torontobusmap;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by giles on 23/09/17.
 */

public class MapDataShapes {
    private List<MapDataShape> shapes;

    public MapDataShapes(InputStream inputStream)
    {
        this.shapes = new ArrayList<>();
        try {
            CSVParser parser = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(new InputStreamReader(inputStream));
            for (CSVRecord record : parser)
            {
                shapes.add(new MapDataShape(record));
            }
            System.out.println("shapes.size = " + shapes.size());
        }
        catch(IOException e)
        {
            System.out.println(e);
        }
    }
}
