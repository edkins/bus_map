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
    public TorontoMapView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    protected void onDraw(Canvas c)
    {
        c.drawRect(new Rect(0,0,200,200), paint());
        //c.drawRGB(255,128,0);
    }

    private Paint paint() {
        Paint p = new Paint();
        p.setColor(0xff456789);
        return p;
    }
}
