package com.example.myrooms;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.view.View;

public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        goToIntruderView();
        goToGasView();
        goToHomeAutomationView();
    }



    private void goToIntruderView() {
        CardView intruderCardView = findViewById(R.id.IntruderCardView);
        intruderCardView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, Intruder.class);
                intent.putExtra("info", "This is activity from card item index  ");
                startActivity(intent);

            }
        });

    }

    private void goToGasView() {
        CardView gasCardView = findViewById(R.id.GasAlarmCardView);
        gasCardView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, gas.class);
                intent.putExtra("info", "This is activity from card item index  ");
                startActivity(intent);

            }
        });

    }

    private void goToHomeAutomationView() {
        CardView homeAutoCardView = findViewById(R.id.HomeAutomationCardView);
        homeAutoCardView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, homeAutomation.class);
                intent.putExtra("info", "This is activity from card item index  ");
                startActivity(intent);

            }
        });

    }

}
