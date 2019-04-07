package com.example.myrooms;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class Intruder extends AppCompatActivity {

    private DatabaseReference databaseReference;//Firebase reference
    public static int getRedPinSeekBarValue;//Gets the value of the seekBar
    public static int getBluePinSeekBarValue;//Gets the value of the seekBar
    TextView redPinseekBarValueTV;
    TextView bluePinseekBarValueTV;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_intruder);
        databaseReference = FirebaseDatabase.getInstance().getReference();

        onButton();
        offButton();
        UpdatePinValues();

        //Seekbar was implemented using this https://stackoverflow.com/questions/8629535/implementing-a-slider-seekbar-in-android
        SeekBar redPinSeekBar = findViewById(R.id.redPinSeekBar);//Assigning seekbar as redPinSeekBar
        redPinSeekBar.setOnSeekBarChangeListener(redPinSeekBarChangeListener);
        final int seekBarValue = redPinSeekBar.getProgress();//Getting value of the seekbar on create of the dweetResponseMessage
        redPinseekBarValueTV = findViewById(R.id.redPinseekBarValue);
        redPinseekBarValueTV.setText("Move to change Red Brightness Level");


        //Seekbar was implemented using this https://stackoverflow.com/questions/8629535/implementing-a-slider-seekbar-in-android
        SeekBar bluePinSeekBar = findViewById(R.id.bluePinSeekBar);//Assigning seekbar as redPinSeekBar
        bluePinSeekBar.setOnSeekBarChangeListener(bluePinSeekBarChangeListener);
        final int seekBarValue2 = bluePinSeekBar.getProgress();//Getting value of the seekbar on create of the dweetResponseMessage
        bluePinseekBarValueTV = findViewById(R.id.bluePinseekBarValue);
        bluePinseekBarValueTV.setText("Move to change Blue Brightness Level");

    }




    private void onButton() {
        Button onButton = findViewById(R.id.onButton);
        onButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                databaseReference.child("motionDetect").setValue("True");

            }
        });
    }

    private void offButton() {
        Button offButton = findViewById(R.id.offButton);
        offButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                databaseReference.child("motionDetect").setValue("False");
            }
        });
    }

    //Method that allows us to update Red and Blue pin values at once with one button click
    private void UpdatePinValues() {
        Button updatePinValue = findViewById(R.id.updatePinValues);
        updatePinValue.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                databaseReference.child("redPin").setValue(getRedPinSeekBarValue);
                databaseReference.child("bluePin").setValue(getBluePinSeekBarValue);
            }
        });
    }




    //https://stackoverflow.com/questions/8629535/implementing-a-slider-seekbar-in-android
    SeekBar.OnSeekBarChangeListener redPinSeekBarChangeListener = new SeekBar.OnSeekBarChangeListener() {

        @Override
        public void onProgressChanged(SeekBar seekBar, int seekBarValue, boolean fromUser) {
            // updated continuously as the user slides the thumb
            redPinseekBarValueTV.setText("Red Brightness Level: " + seekBarValue);
            getRedPinSeekBarValue = seekBarValue;

        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {
            // called when the user first touches the SeekBar
        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
            // called after the user finishes moving the SeekBar
        }
    };

    //https://stackoverflow.com/questions/8629535/implementing-a-slider-seekbar-in-android
    SeekBar.OnSeekBarChangeListener bluePinSeekBarChangeListener = new SeekBar.OnSeekBarChangeListener() {

        @Override
        public void onProgressChanged(SeekBar seekBar, int seekBarValue, boolean fromUser) {
            // updated continuously as the user slides the thumb
            bluePinseekBarValueTV.setText("Blue Brightness Level: " + seekBarValue);
            getBluePinSeekBarValue = seekBarValue;

        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {
            // called when the user first touches the SeekBar
        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
            // called after the user finishes moving the SeekBar
        }
    };




}
