package io.pantheist.torontobusmap;

import android.graphics.Canvas;
import android.graphics.Paint;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by giles on 23/09/17.
 */

public class MapPresentationRoute {
    public List<MapPresentationPoint> points;

    public MapPresentationRoute()
    {
        this.points = new ArrayList<>();
    }

    public void draw(Canvas c, Paint paint)
    {
        for (int i = 0; i < points.size()-1; i++)
        {
            c.drawLine(points.get(i).x, points.get(i).y, points.get(i+1).x, points.get(i+1).y, paint);
        }
    }
}
