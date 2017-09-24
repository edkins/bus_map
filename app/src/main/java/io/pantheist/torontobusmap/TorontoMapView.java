package io.pantheist.torontobusmap;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.view.View;

/**
 * Created by giles on 23/09/17.
 */

public class TorontoMapView extends View {
    private final MapPresentation presentation;

    public TorontoMapView(Context context, AttributeSet attrs) {
        super(context, attrs);

        MapData data = new MapData( context.getResources() );
        presentation = new MapPresentation(data, bounds());
    }

    private MapPresentationBounds bounds() {
        return new MapPresentationBounds(360,500);
    }

    @Override
    protected void onDraw(Canvas c)
    {
        presentation.draw(c);
    }
}
