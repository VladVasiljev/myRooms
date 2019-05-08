package com.example.myrooms;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class homeAutomation extends AppCompatActivity {

    private DatabaseReference databaseReference;//Firebase reference

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_automation);
        databaseReference = FirebaseDatabase.getInstance().getReference();//Getting database reference

        pcOff();
        pcOn();
    }


    private void pcOn() {//Method that turns on the PC
        Button computerOn = findViewById(R.id.onButton);//Assigning button to computerOn
        computerOn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                databaseReference.child("computerRelaySwitch").setValue(1);
            }
        });
    }

    private void pcOff() {//Method that turns off the PC
        Button computerOff = findViewById(R.id.offButton);//Assigning a button to computer off
        computerOff.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                databaseReference.child("computerRelaySwitch").setValue(1);

            }
        });
    }



}
