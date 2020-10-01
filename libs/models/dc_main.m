
function [current_rate] = dc_main(embb_num, total_RB, y_start_end, embb_rate, embb_rb_ass, urllc_num, urllc_rb_perusr, drc)


Y = zeros(embb_num, total_RB);
y = (reshape(y_start_end', 2, embb_num)).';
for n = 1: embb_num
  length = y(n, 2) - y(n, 1) + 1;
  for k = y(n, 1):y(n, 2)
    Y(n, k) = 1;
  end
end


[X, T] = cccp(total_RB, Y, embb_num, urllc_num, embb_rb_ass, urllc_rb_perusr, y,embb_rate, drc);

%Utility = sum(T);
current_rate = T;
end

