`define BUF_WIDTH 3    // BUF_SIZE = 16 -> BUF_WIDTH = 4, no. of bits to be used in pointer
`define BUF_SIZE ( 1<<`BUF_WIDTH )

module fifo( clk, rst, data_in, data_out, push, pop, empty, full, fifo_counter );

// reset, system clock, write enable and read enable.
input                 rst, clk, push, pop;   

// data input to be pushed to buffer
input [7:0]           data_in;                   

// port to output the data using pop.
output[7:0]           data_out;                  

// buffer empty and full indication 
output                empty, full;      

// number of data pushed in to buffer 
output[`BUF_WIDTH :0] fifo_counter;             
  

reg[7:0]              data_out;
reg                   empty, full;
reg[`BUF_WIDTH :0]    fifo_counter;
reg[`BUF_WIDTH -1:0]  read_pointer, write_pointer;           // pointer to read and write addresses  
reg[7:0]              memory[`BUF_SIZE -1 : 0]; //  

always @(fifo_counter)
begin
   empty = (fifo_counter == 0);
   full = (fifo_counter == `BUF_SIZE);

end

always @(posedge clk or posedge rst)
begin
   if( rst )
       fifo_counter <= 0;

   else if( (!full && push) && ( !empty && pop ) )
       fifo_counter <= fifo_counter;

   else if( !full && push )
       fifo_counter <= fifo_counter + 1;

   else if( !empty && pop )
       fifo_counter <= fifo_counter - 1;
   else
      fifo_counter <= fifo_counter;
end

always @( posedge clk or posedge rst)
begin
   if( rst )
      data_out <= 0;
   else
   begin
      if( pop && !empty )
         data_out <= memory[read_pointer];

      else
         data_out <= data_out;

   end
end

always @(posedge clk)
begin

   if( push && !full )
      memory[ write_pointer ] <= data_in;

   else
      memory[ write_pointer ] <= memory[ write_pointer ];
end

always@(posedge clk or posedge rst)
begin
   if( rst )
   begin
      write_pointer <= 0;
      read_pointer <= 0;
   end
   else
   begin
      if( !full && push )    write_pointer <= write_pointer + 1;
      else  write_pointer <= write_pointer;

      if( !empty && pop )   read_pointer <= read_pointer + 1;
      else read_pointer <= read_pointer;
   end

end
endmodule
