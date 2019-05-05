package com.example.myrooms;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.widget.Button;
import android.widget.TextView;

import com.example.myrooms.Models.modelDatabase;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class gas extends AppCompatActivity {

    private DatabaseReference databaseReference;//Firebase reference
    private ValueEventListener databaseListener;
    private int count = 0;
    Animation anim = new AlphaAnimation(0.0f, 1.0f);
    private static int view = 2;
    TextView smokeValue,CarbonMonoValue,smokeDensity,CarbonMonoDensity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gas);
        databaseReference = FirebaseDatabase.getInstance().getReference();

        smokeValue = findViewById(R.id.smokeValue);
        CarbonMonoValue = findViewById(R.id.CarbonMonoValue);
        smokeDensity = findViewById(R.id.smokeDensity);
        CarbonMonoDensity = findViewById(R.id.CarbonMonoDensity);

        onButton();
        offButton();


        //Saving the state of the notification method
        if (view == 1) {

            notifcationOn();
            view = 1;
            Log.d("myTag", "" + view);
        } else if (view == 0) {
            notifcationOff();
            view = 0;
            Log.d("myTag", "" + view);
        }

    }

    @Override
    protected void onStart() {
        super.onStart();
        //Computer Name from FireBase
        ValueEventListener databaseListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                if (dataSnapshot.exists()) {
                    modelDatabase databaseReader = dataSnapshot.getValue(modelDatabase.class);


                    smokeValue.setText(String.valueOf(databaseReader.mq2sensorValue));
                    smokeDensity.setText(String.valueOf(databaseReader.mq2sensorDensity));
                    CarbonMonoValue.setText(String.valueOf(databaseReader.mq9sensorValue));
                    CarbonMonoDensity.setText(String.valueOf(databaseReader.mq9sensorDensity));
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                // Failed to read value
                //Log.e(TAG, "onCancelled: Failed to read message");

                smokeValue.setText("Not Found");
                smokeDensity.setText("Not Found");
                CarbonMonoDensity.setText("Not Found");
                CarbonMonoValue.setText("Not Found");
            }
        };
        databaseReference.addValueEventListener(databaseListener);

        // copy for removing at onStop()
        this.databaseListener = databaseListener;
    }

    //When the on button is clicked, we do the following, set value to true and call the notificationOn method.
    private void onButton() {
        Button onButton = findViewById(R.id.onButton);
        onButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                databaseReference.child("setGasAlarm").setValue("True");
                notifcationOn();
            }
        });
    }
    //When the off button is clicked, we do the following, set value to true and call the notificationOff method.
    private void offButton() {
        Button offButton = findViewById(R.id.offButton);
        offButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                databaseReference.child("setGasAlarm").setValue("False");
                notifcationOff();

            }
        });
    }

    //Method which turns on the notification
    private void notifcationOn() {
        TextView notificationOff = findViewById(R.id.notficationOff);
        TextView notificationOn = findViewById(R.id.notficationOn);
        notificationOn.setVisibility(View.VISIBLE);
        notificationOff.setVisibility(View.GONE);
        notificationOn.setText("Gas System is activated");
        view = 1;
        if (count == 0) {
            anim.cancel();
        }

    }
    //Method which turns off the notification
    private void notifcationOff() {
        TextView notificationOn = findViewById(R.id.notficationOn);
        TextView notificationOff = findViewById(R.id.notficationOff);
        notificationOn.setVisibility(View.GONE);
        notificationOff.setVisibility(View.VISIBLE);
        notificationOff.setText("Gas System is deactivated");
        view = 0;
        anim.setDuration(500); //You can manage the blinking time with this parameter
        anim.setStartOffset(100);
        anim.setRepeatMode(Animation.REVERSE);
        anim.setRepeatCount(Animation.INFINITE);
        notificationOff.startAnimation(anim);
    }
}
