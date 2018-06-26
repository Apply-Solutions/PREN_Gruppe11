package com.example.koru.t11_pren1;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.util.TypedValue;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.time.LocalTime;
import java.util.Timer;
import java.util.TimerTask;
import java.util.UUID;

public class MainActivity extends AppCompatActivity{
    private TextView txtLog;
    private TextView txtStatus;
    private TextView txtSteps;
    private TextView txtTime;
    private TextView txtRobotPosX;
    private TextView txtCargo;
    private TextView txtCargoPosX;
    private TextView txtCargoPosY;
    private Button cmdStart;
    private Button cmdConnect;

    private Timer timer;

    private int timeInSec;
    public Handler mHandler = new Handler() {
        public void handleMessage(Message message) {
            System.out.println(message.arg1 + " " + message.arg2);
            String formattedResource;
            formattedResource = String.format(getResources().getString(R.string.time), showTwoDigits(message.arg1), showTwoDigits(message.arg2));

            txtTime.setText(formattedResource);
        }
    };

    private boolean cargo = false;

    private BluetoothAdapter btAdapter;
    private BluetoothDevice device;

    private BluetoothSocket btSocket;
    private AsyncTask<BluetoothSocket, Void, String> readerTask;

    private boolean errorDetected = false;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtLog = (TextView)findViewById(R.id.txtLog);
        txtLog.setMovementMethod(new ScrollingMovementMethod());
        txtStatus = (TextView)findViewById(R.id.txtStatus);
        txtTime = (TextView)findViewById(R.id.txtTime);
        txtRobotPosX = (TextView)findViewById(R.id.txtRobotPosX);
        txtCargo = (TextView)findViewById(R.id.txtCargo);
        txtCargoPosX = (TextView)findViewById(R.id.txtCargoPosX);
        txtCargoPosY = (TextView)findViewById(R.id.txtCargoPosY);
        txtSteps = (TextView)findViewById(R.id.txtSteps);
        cmdStart = (Button)findViewById(R.id.cmdStartProcess);
        cmdConnect = (Button)findViewById(R.id.cmdConnect);

        System.out.println();
    }

    @Override
    protected void onDestroy() {
        readerTask.cancel(true);

        String message = "disconnect";

        try {
            OutputStream oStream = btSocket.getOutputStream();
            oStream.write(message.getBytes());
            oStream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

        super.onDestroy();
    }

    public void startProcess(View o) {
        if (!btSocket.isConnected()) { System.out.println("no connection"); return; }
        int steps_in_mm = Integer.parseInt(txtSteps.getText().toString());
        System.out.println("Value in mm: " + steps_in_mm);
        String message = "start-process@" + convert_mm_to_steps(steps_in_mm);
        System.out.println("Value in steps: " + message);

        try {
            OutputStream oStream = btSocket.getOutputStream();
            oStream.write(message.getBytes());
            oStream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

        timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
            timeInSec++;

            int min, sec;
            min = timeInSec / 60;
            sec = timeInSec % 60;

            mHandler.obtainMessage(1,min, sec).sendToTarget();
            }
        }, 0, 1000);

        cmdStart.setEnabled(false);
    }

    public void connectBT(View o) {
        Log.d("Method", "OK");

        btAdapter = BluetoothAdapter.getDefaultAdapter();

        Log.d("Bluetoothadapter", btAdapter.getName());
        device = btAdapter.getBondedDevices().iterator().next();

        Log.d("Device", "Got bonded device: " + device);

        try {
            btSocket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001105-0000-1000-8000-00805f9b34fb"));
            btAdapter.cancelDiscovery();

            Log.d("Socket", "Socket created:" + btSocket);
            txtStatus.setText(getResources().getString(R.string.status_connected));
            try {
                btSocket.connect();
                Log.e("","Connected");
            } catch (IOException e) {
                Log.e("",e.getMessage());

                try {
                    Log.e("","trying fallback...");

                    btSocket =(BluetoothSocket) device.getClass().getMethod("createRfcommSocketToServiceRecord", new Class[] {int.class}).invoke(device,1);
                    btSocket.connect();

                    Log.e("","Connected");
                }
                catch (Exception e2) {
                    Log.e("", "Couldn't establish Bluetooth connection!");
                }
            }

            if (btSocket.isConnected()) {
                Log.d("ReaderTask", "Starting reader...");
                readerTask = new BluetoothReader().execute(btSocket);
                txtStatus.setText(getResources().getString(R.string.status_connected));
                cmdStart.setEnabled(true);
                cmdConnect.setEnabled(false);
            } else {
                txtStatus.setText(getResources().getString(R.string.status_error));
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private int convert_mm_to_steps(float mm) {
        float y = mm / 10f;
        return (int) Math.round(-100*(Math.sqrt(-1000*(y - 2215.269))-1480));
    }

    private float convert_x_steps_to_mm(int steps) {
        //return (float) (2215.269 + (Math.pow(1480 + steps / -100, 2) / -1000));
        return (float) (-Math.pow(10, -7) * Math.pow(steps, 2) + 0.0296 * steps + 24.868);
    }

    private float convert_y_steps_to_mm(int steps) {
        return (float) ((-2 * Math.pow(10, -12) * Math.pow(steps, 3)) + (4 * Math.pow(10, -7) * Math.pow(steps, 2)) + (0.0004 * steps) + 35.508);
    }

    private float recalculateDistance(float distance) {
        return distance / 10;
    }

    private float convert_mm_to_pixels(float mm) {
        return TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_MM, 1,
                getResources().getDisplayMetrics()) * mm;
    }

    private String showTwoDigits(int number) {
        return String.format("%02d", number);
    }

    private String getResourceString(Integer res) {
        return getResources().getString(res);
    }

    private class BluetoothReader extends AsyncTask<BluetoothSocket, Void, String>  {
        @Override
        protected String doInBackground(BluetoothSocket... params) {
            BluetoothSocket btSocket = params[0];
            InputStream iStream;
            int iMsg;
            String sMsg = "";

            try {
                Log.d("BluetoothReader", "Is connected:" + btSocket.isConnected());
                while (!errorDetected) {
                    iStream = btSocket.getInputStream();

                    while((iMsg = iStream.read())!=-1) {
                        // converts integer to character
                        char charMsg = (char)iMsg;

                        if (charMsg != '#') {
                            sMsg += charMsg;
                        } else {
                            return sMsg;
                        }
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
                errorDetected = true;
            }

            return "";
        }

        @Override
        protected void onPostExecute(String s) {
            Log.d("BluetoothReader", "Received message from server: " + s);
            String message = s.toLowerCase();


            if (message.contains("status") && message.contains("started")) {
                cmdStart.setEnabled(false);
            } else if (message.contains("position")) {
                String[] arrSplitter = s.split("@");
                String[] arrMessage = arrSplitter[1].split(";");

                int stepsX = Integer.parseInt(arrMessage[1]);
                int stepsY = Integer.parseInt(arrMessage[2]);
                float distanceX = convert_x_steps_to_mm(stepsX);
                float distanceY = convert_y_steps_to_mm(stepsX);

                txtRobotPosX.setText(String.format(getResourceString(R.string.robot_pos), String.valueOf(distanceX) + " (" + String.valueOf(stepsX) + ")"));

                if (cargo) {
                    txtCargoPosX.setText(String.format(getResourceString(R.string.cargo_posX), String.valueOf(distanceX) + " (" + String.valueOf(stepsX) + ")"));
                    txtCargoPosY.setText(String.format(getResourceString(R.string.cargo_posY), String.valueOf(distanceY) + " (" + String.valueOf(stepsX) + ")"));
                }
            } else if (message.contains("event") && message.contains("collision")) {
                timer.cancel();
                timer.purge();
            } else if (message.contains("event") && message.contains("cargo") && message.contains("picked up")) {
                cargo = true;
                txtCargo.setText(String.format(getResourceString(R.string.cargo), "Ja"));
            } else if (message.contains("event") && message.contains("cargo") && message.contains("at destination")){
                cargo = false;
                txtCargo.setText(String.format(getResourceString(R.string.cargo), "Nein"));
            } else {
                txtLog.append(s + "\n");
            }

            readerTask = new BluetoothReader().execute(btSocket);
        }
    }
}
