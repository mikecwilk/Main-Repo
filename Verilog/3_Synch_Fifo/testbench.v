module testbench(

    );
    
reg           clk;
reg           rst; 
reg           push;
reg           pop;       
reg [7:0]     data_in;
wire [7:0]    data_out;
wire          empty;        
wire          almost_empty;
wire          full;
wire          almost_full; 

fifo fifo_0
            (.clk           (clk),
            .rst            (rst),
            .push           (push),
            .pop            (pop),
            .data_in        (data_in),
            .data_out       (data_out),
            .empty          (empty),
            .almost_empty   (almost_empty),
            .full           (full),
            .almost_full    (almost_full)
            );

initial begin            
    clk = 0;
    rst = 1;
    push = 0;
    pop = 0;
//Fill the FIFO
    data_in = 8'b10101010;//1
    #10
    rst = 0;
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b11111010;//2
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b10101111;//3
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b11111111;//4
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b00000000;//5
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b00000001;//6
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b00000010;//7
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b00000100;//8
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b00000100;//9
    #10
    push = 1;
    #10
    push = 0;
    data_in = 8'b00001000;//10
    #10
    push = 1;
    #60
    push = 0;
    #10 
    pop = 1;//1
    #10
    pop = 0;
    #40 
    pop = 1;//2
    #10
    pop = 0;
    #40 
    pop = 1;//3
    #10
    pop = 0;
    #40 
    pop = 1;//4
    #10
    pop = 0;
    #40 
    pop = 1;//5
    #10
    pop = 0;
    #40 
    pop = 1;//6
    #10
    pop = 0;
    #40 
    pop = 1;//7
    #10
    pop = 0;
    #40 
    pop = 1;//8
    #10
    pop = 0;
    #40 
    pop = 1;//9
    #10
    pop = 0;
    #40 
    pop = 1;//10
    #10
    pop = 0;
end
always begin
clk = #5 !clk;
end
  
endmodule
