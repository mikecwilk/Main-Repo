`define BUF_WIDTH 3    // BUF_SIZE = 16 -> BUF_WIDTH = 4, no. of bits to be used in pointer
`define BUF_SIZE ( 1<<`BUF_WIDTH )

module testbench();

reg                 rst, clk, push, pop;   

reg [7:0]           data_in;                   

// port to output the data using pop.
wire[7:0]           data_out;                  

// buffer empty and full indication 
wire                empty, full;      

// number of data pushed in to buffer 
wire[`BUF_WIDTH :0] fifo_counter;  

fifo fifo_0
            (.rst       (rst),
            .clk        (clk),
            .push       (push),
            .pop        (pop),
            .data_in    (data_in),
            .data_out   (data_out),
            .empty      (empty),
            .full       (full),
            .fifo_counter   (fifo_counter)
            );

initial begin

rst = 1'b1;
clk = 1'b0;
push = 1'b0;
pop = 1'b0;
data_in = 8'b11111111;

#10
rst = 1'b0;

#10
push = 1'b1;//1
#10 
push = 1'b0;
data_in = 8'b11110000;

#10
push = 1'b1;//2
#10 
push = 1'b0;
data_in = 8'b11111010;

#10
push = 1'b1;//3
#10 
push = 1'b0;
data_in = 8'b10101010;

#10
push = 1'b1;//4
#10 
push = 1'b0;
data_in = 8'b11110001;

#10
push = 1'b1;//5
#10 
push = 1'b0;
data_in = 8'b00001111;

#10
push = 1'b1;//6
#10 
push = 1'b0;
data_in = 8'b11110101;

#10
push = 1'b1;//7
#10 
push = 1'b0;
data_in = 8'b00000101;

#10
push = 1'b1;//8
#10 
push = 1'b0;
data_in = 8'b00010101;

#10
push = 1'b1;//9
#10 
push = 1'b0;
data_in = 8'b00000000;

#10
push = 1'b1;//10
#10 
push = 1'b0;
data_in = 8'b11111111;

#10
push = 1'b1;//10
#10 
push = 1'b0;
data_in = 8'b00000000;

#40

pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;
#10
pop = 1'b1;
#10
pop = 1'b0;

#50
pop = 1'b1;
#10
pop = 1'b0;
end



always begin
clk = #5 !clk;
end
endmodule
