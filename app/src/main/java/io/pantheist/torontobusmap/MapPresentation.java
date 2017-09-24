package io.pantheist.torontobusmap;

import android.graphics.Canvas;
import android.graphics.Paint;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by giles on 23/09/17.
 */

public class MapPresentation {
    private final MapData data;
    public final List<MapPresentationRoute> routes;
    private final MapPresentationBounds presentationBounds;

    public MapPresentation(MapData data, MapPresentationBounds presentationBounds)
    {
        this.data = data;
        this.presentationBounds = presentationBounds;

        this.routes = new ArrayList<>();
        addRoutes();
    }

    private void addRoutes() {
        int shape_id = -1;
        MapBounds bounds = data.shapes.bounds();

        for (MapDataShape shape : data.shapes.shapes)
        {
            MapPresentationRoute route;
            if (shape.shape_id != shape_id)
            {
                route = new MapPresentationRoute();
                routes.add(route);
            }
            else
            {
                route = routes.get(routes.size()-1);
            }
            shape_id = shape.shape_id;
            route.points.add(shape.presentationPoint(bounds, presentationBounds));
        }
    }

    public void draw(Canvas c)
    {
        Paint paint = paint();
        for (MapPresentationRoute route : routes)
        {
            route.draw(c, paint);
        }
    }

    private Paint paint() {
        Paint p = new Paint();
        p.setColor(0xff456789);
        return p;
    }
}
