clear;

dpick1 = py.DynPick.DynPick('COM5'); % ポート番号は適宜変更すること
dpick2 = py.DynPick.DynPick('COM6');
dpick3 = py.DynPick.DynPick('COM7');

% % dpick1.show_firmware_version();
% dpick1.show_sensitivity();
% dpick2.show_sensitivity();
% dpick3.show_sensitivity();
% disp(string(dpick1.read_temperature())+'(deg C)');
% disp(string(dpick2.read_temperature())+'(deg C)');
% disp(string(dpick3.read_temperature())+'(deg C)');
% disp(string(dpick4.read_temperature())+'(deg C)');

% data = dpick1.read_once();
% disp(double(data));
% disp("[N], [Nm]");
dpick1.set_sensitivity();
dpick2.set_sensitivity();
dpick3.set_sensitivity();

dpick1.start_continuous_read();
dpick2.start_continuous_read();
dpick3.start_continuous_read();
tt=[];

    s0_1 = double(dpick1.read_continuous());
    s0_2 = double(dpick2.read_continuous());
    s0_3 = double(dpick3.read_continuous());
tic;

t=20;
port1=[];
port2=[];
port3=[];
for v=1:100
    data1 = dpick1.read_continuous();
    data2 = dpick2.read_continuous();
    data3 = dpick3.read_continuous();
    pause(0.1);
    tt = [tt; toc];
    port1 = [port1; double(data1)-s0_1];
    port2 = [port2; double(data2)-s0_2];
    port3 = [port3; double(data3)-s0_3];
    % disp(v);
end
toc


time_data=[tt,port1,port2,port3];
save("time_data", "time_data");
% time_data2=[tt,port2];
% save("time_data2", "time_data2");
% time_data3=[tt,port3];
% save("time_data3", "time_data3");

% x=time_data(:,1);
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% y11=-time_data(:,4);
% figure(1);
% plot(x,y11,'-o');
% % xlavel('時間');
% % ylavel('z方向の推力');
% grid on;
% % disp(double(data));
% % disp("[t], [N]");

figure(1);clf;hold('on');
plot(time_data(:,1), -time_data(:,4),"LineWidth",2,"Color","r"); %1
fontsize(16,"points")
xlabel('Time[s]','FontSize',16)
ylabel('Force[N]','FontSize',16)
title('A')


figure(2);clf;hold('on');
plot(time_data(:,1), -time_data(:,10),"LineWidth",2,"Color","r"); %1
fontsize(16,"points")
xlabel('Time[s]','FontSize',16)
ylabel('Force[N]','FontSize',16)
title('B')


figure(3);clf;hold('on');
plot(time_data(:,1), -time_data(:,16),"LineWidth",2,"Color","r"); %1
fontsize(16,"points")
xlabel('Time[s]','FontSize',16)
ylabel('Force[N]','FontSize',16)
title('C')



% y12=-time_data(:,10);
% figure(2);
% plot(x,y12,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% % disp(double(data));
% % disp("[t], [Nm]");
% 
% y13=-time_data(:,16);
% figure(3);
% plot(x,y13,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% disp(double(data));
% disp("[t], [Nm]");

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% y21=-time_data2(:,4);
% figure(4);
% plot(x,y21,'-o');
% % xlavel('時間');
% % ylavel('z方向の推力');
% grid on;
% % disp(double(data));
% % disp("[t], [N]");
% 
% y22=-time_data2(:,5);
% figure(5);
% plot(x,y22,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% % disp(double(data));
% % disp("[t], [Nm]");
% 
% y23=-time_data2(:,6);
% figure(6);
% plot(x,y23,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% % disp(double(data));
% % disp("[t], [Nm]");
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% y31=-time_data3(:,4);
% figure(7);
% plot(x,y31,'-o');
% % xlavel('時間');
% % ylavel('z方向の推力');
% grid on;
% % disp(double(data));
% % disp("[t], [N]");
% 
% y32=-time_data3(:,5);
% figure(8);
% plot(x,y32,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% % disp(double(data));
% % disp("[t], [Nm]");
% 
% y33=-time_data3(:,6);
% figure(9);
% plot(x,y33,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% % disp(double(data));
% % disp("[t], [Nm]");
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% y41=-time_data4(:,4);
% figure(10);
% plot(x,y41,'-o');
% % xlavel('時間');
% % ylavel('z方向の推力');
% grid on;
% % disp(double(data));
% % disp("[t], [N]");
% 
% y42=-time_data4(:,5);
% figure(11);
% plot(x,y42,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% % disp(double(data));
% % disp("[t], [Nm]");
% 
% y43=-time_data4(:,6);
% figure(12);
% plot(x,y43,'-o');
% % xlavel('時間');
% % ylavel('トルク');
% grid on;
% % disp(double(data));
% % disp("[t], [Nm]");