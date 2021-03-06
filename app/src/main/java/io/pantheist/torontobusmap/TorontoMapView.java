package io.pantheist.torontobusmap;

import android.content.Context;
import android.graphics.Canvas;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.ScaleGestureDetector;
import android.view.View;

/**
 * Created by giles on 23/09/17.
 */

public class TorontoMapView extends View implements ScaleGestureDetector.OnScaleGestureListener {
    private final MapPresentation presentation;

    private final ScaleGestureDetector scaleDetector;

    public TorontoMapView(Context context, AttributeSet attrs) {
        super(context, attrs);

        MapData data = new MapData( context.getResources() );
        presentation = new MapPresentation(data, bounds());

        this.scaleDetector = new ScaleGestureDetector(context,this);

    }

    private MapPresentationBounds bounds() {
        return new MapPresentationBounds(360,500);
    }

    @Override
    protected void onDraw(Canvas c)
    {
        presentation.draw(c);
    }

    @Override
    public boolean onTouchEvent(MotionEvent ev) {
        // Let the ScaleGestureDetector inspect all events.
        scaleDetector.onTouchEvent(ev);
        return true;
    }

    @Override
    public boolean onScale(ScaleGestureDetector scaleGestureDetector) {
        System.out.println("scale " + scaleGestureDetector.getScaleFactor());
        return true;
    }

    @Override
    public boolean onScaleBegin(ScaleGestureDetector scaleGestureDetector) {
        return true;
    }

    @Override
    public void onScaleEnd(ScaleGestureDetector scaleGestureDetector) {

    }
}
