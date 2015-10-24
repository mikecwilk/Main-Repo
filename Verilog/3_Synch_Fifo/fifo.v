module fifo(
        clk,
        rst,
        push,
        pop,
        data_in,
        data_out,
        empty,
        almost_empty,
        full,
        almost_full
        );

input           clk;
input           rst; 
input           push;
input           pop;       
input [7:0]     data_in;
output reg [7:0]    data_out;
output reg         empty;        
output reg         almost_empty;
output reg         full;
output reg         almost_full;

reg [3:0]       read_pointer;
reg [3:0]       write_pointer;
reg [7:0]       memory[9:0];

always @(*)
    begin
        if(write_pointer == 4'b1010)
            begin
                full = 'b1;
                almost_full = 'b1;
                empty = 'b0;
                almost_empty = 'b0;
            end

        else if(write_pointer == 4'b0000)
            begin
                full = 'b0;
                almost_full = 'b0;
                empty = 'b1;
                almost_empty = 'b1;               
            end
        else if (write_pointer == 4'b01001)
            begin
                full = 'b0;
                almost_full = 'b1;
                empty = 'b0;
                almost_empty = 'b0; 
            end
        else if (write_pointer == 4'b0010)
             begin
                 full = 'b0;
                 almost_full = 'b0;
                 empty = 'b0;
                 almost_empty = 'b1; 
             end
        else if (write_pointer > 4'b0010 && write_pointer < 4'b1000)
            begin
                full = 'b0;
                almost_full = 'b0;
                empty = 'b0;
                almost_empty = 'b0; 
            end
    end

always @(posedge clk or negedge rst)
    begin
        if(rst)
            begin
            read_pointer <= 4'b0000;
            write_pointer <= 4'b0000;
            end
        else if(push && !full)
            begin
                memory[write_pointer] <= data_in;
                write_pointer <= write_pointer + 'b1;
            end
        else if(pop && !empty)
            begin
                data_out <= memory[read_pointer];
                
                write_pointer <= write_pointer - 'b1;
                memory[0] <= memory[1];
                memory[1] <= memory[2];
                memory[2] <= memory[3];
                memory[3] <= memory[4];
                memory[4] <= memory[5];
                memory[5] <= memory[6];
                memory[6] <= memory[7];
                memory[7] <= memory[8];
                memory[8] <= memory[9];
                memory[9] <= memory[10];
                
            end
            
            
    end
endmodule
