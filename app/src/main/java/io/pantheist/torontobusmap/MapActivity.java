package io.pantheist.torontobusmap;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class MapActivity extends AppCompatActivity {
    MapData data;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        data = new MapData(getResources());

        setContentView(R.layout.activity_map);


    }

}
