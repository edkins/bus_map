package io.pantheist.torontobusmap;

/**
 * Created by giles on 23/09/17.
 */

public class MapBounds {
    public final float minLon;

    public final float minLat;

    public final float maxLon;

    public final float maxLat;

    public MapBounds(float minLon, float minLat, float maxLon, float maxLat)
    {
        this.minLon = minLon;
        this.minLat = minLat;
        this.maxLon = maxLon;
        this.maxLat = maxLat;
    }

    public MapBounds expand(MapBounds other)
    {
        if (other == null)
        {
            return this;
        }
        return new MapBounds(
                Math.min(minLon, other.minLon),
                Math.min(minLat, other.minLat),
                Math.max(maxLon, other.maxLon),
                Math.max(maxLat,other.maxLat)
        );
    }

    public MapPresentationPoint scale(float lon, float lat, MapPresentationBounds bounds)
    {
        return new MapPresentationPoint(
                bounds.width * (lon-minLon)/(maxLon-minLon),
                bounds.height * (lat-minLat)/(maxLat-minLat));
    }
}
