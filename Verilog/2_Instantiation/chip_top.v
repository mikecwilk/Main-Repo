module chip_top(
        ctop_in1,
        ctop_in2,
        ctop_in3,
        ctop_in4,
        ctop_in5,
        ctop_out1,
        ctop_out2,
        ctop_out3,
        ctop_out4
    );

//--------------------------------------- 

input   [7:0]       ctop_in1;
input               ctop_in2;
input               ctop_in3;
input               ctop_in4;
input               ctop_in5;
output              ctop_out1;
output              ctop_out2;
output  [7:0]       ctop_out3;
output              ctop_out4;

//--------------------------------------- 
//wire declaration

wire                xmit_top_0_s1;
wire                rcv_top_0_s1;

//modules instantiation

xmit_top            xmit_top_0
                    (.xmit_top_in1          (ctop_in1),
                    .xmit_top_in2           (ctop_in2),
                    .xmit_top_in3           (ctop_in3),
                    .xmit_top_in4           (rcv_top_0_s1),
                    .xmit_top_out1          (ctop_out1),
                    .xmit_top_out2          (ctop_out2),
                    .xmit_top_out3          (xmit_top_0_s1)
                    );
                    
rcv_top             rcv_top_0
                    (.rcv_top_in1           (ctop_in4),
                    .rcv_top_in2            (ctop_in5),
                    .rcv_top_in3            (xmit_top_0_s1),
                    .rcv_top_out1           (ctop_out3),
                    .rcv_top_out2           (ctop_out4),
                    .rcv_top_out3           (rcv_top_0_s1)
                    );             

endmodule
