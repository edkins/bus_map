package io.pantheist.torontobusmap;

import android.content.res.Resources;

import java.io.IOException;
import java.io.InputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

/**
 * Created by giles on 23/09/17.
 */

public class MapData {

    public MapDataShapes shapes;

    public MapData(Resources resources)
    {
        InputStream resourceStream = resources.openRawResource(R.raw.opendata_ttc_schedules);

        try (ZipInputStream zip = new ZipInputStream(resourceStream)) {

            while(true) {
                ZipEntry entry = zip.getNextEntry();
                if (entry == null) break;
                String name = entry.getName();

                if (name.equals("shapes.txt")) {
                    shapes = new MapDataShapes(zip);
                }
                System.out.println(name);

                zip.closeEntry();
            }
        }
        catch(IOException e)
        {
            System.out.println(e);
        }
    }

}
