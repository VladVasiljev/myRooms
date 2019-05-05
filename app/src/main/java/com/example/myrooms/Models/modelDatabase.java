package com.example.myrooms.Models;

import com.google.firebase.database.Exclude;
import com.google.firebase.database.IgnoreExtraProperties;

import java.util.HashMap;
import java.util.Map;

@IgnoreExtraProperties
public class modelDatabase {
    public int mq2sensorValue;
    public double mq2sensorDensity;
    public int mq9sensorValue;
    public double mq9sensorDensity;


    public modelDatabase() {
    }

    public modelDatabase(int mq2sensorvalue, double mq2sensordensity, int mq9sensorvalue, double mq9sensordensity) {
        this.mq2sensorValue = mq2sensorvalue;
        this.mq2sensorDensity = mq2sensordensity;
        this.mq9sensorValue = mq9sensorvalue;
        this.mq9sensorDensity = mq9sensordensity;

    }

    @Exclude
    public Map<String, Object> toMap() {
        HashMap<String, Object> result = new HashMap<>();
        result.put("mq2sensorValue", mq2sensorValue);
        result.put("mq2sensorDensity", mq2sensorDensity);
        result.put("mq9sensorValue", mq9sensorValue);
        result.put("mq9sensorDensity", mq9sensorDensity);


        return result;
    }
}