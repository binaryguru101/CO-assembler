#dictionary -->  instruction:(func 3,opcode,func7)
Rtype={
    "add":("000","0110011","0000000"),
    "sub":("000","0110011","0100000"),
    "sll":("001","0110011","0000000"),
    "slt":("010","0110011","0000000"),
    "sltu":("011","0110011","0000000"),
    "xor":("100","0110011","0000000"),
    "srl":("101","0110011","0000000"),
    "or":("110","0110011","0000000"),
    "and":("111","0110011","0000000")
}

#dictionary -->  instruction:(func 3,opcode)
Itype={
    "lw":("010","0000011"),
    "addi":("000","0010011"),
    "sltiu":("011","0010011"),
    "jalr":("000","1100111")
}

#dictionary -->  instruction:(func 3,opcode)
Stype={
    "sw":("010","0100011")
}

#dictionary -->  instruction:(func 3,opcode)
Btype={
    "beq": ("000", "1100011"),
    "bne": ("001", "1100011"),
    "blt": ("100", "1100011"),
    "bge": ("101", "1100011"),
    "bltu": ("110", "1100011"),
    "bgeu": ("111", "1100011")
}

#dictionary -->  instruction:(opcode)
Utype={
    "lui":("0110111"),
    "auipc":("0010111")
}

#dictionary -->  instruction:(opcode)
Jtype={
    "jal":("1101111"),
}


register_address= {
    "zero": "00000",      #zero Hard-wired zero 
    "ra": "00001",      #ra   Return Adress
    "sp": "00010",      #sp   Stack pointer
    "gp": "00011",      #gp   Global pointer
    "tp": "00100",      #tp   Thread pointer
    "t0": "00101",      #t0   Temporary reg

    "t1": "00110",      #t1,t2  temporaries
    "t2": "00111",

    "s0": "01000",      #s0,s1   saved registers
    "fp": "01000",
    "s1": "01001",      

    "a0": "01010",     #a0,a1  Function arguments/ returnvalues
    "a1": "01011",

    "a2": "01100",     #a2-a7  Function Arguments
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",

    "s2": "10010",     #s2-s11  saved registers
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",

    "t3": "11100",     #t3-t6    temporatries
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}

# *******************************************************

labels={}
# *******************************************************

program_memory=["00000000","00000004","00000008","0000000c","00000010","00000014","00000018","0000001c","00000020","00000024","00000028","0000002c","00000030","00000034","00000038","0000003c","00000040","00000044","00000048","0000004c","00000050","00000054","00000058","0000005c","00000060","00000064","00000068","0000006c","00000070","00000074","00000078","0000007c","00000080","00000084","00000088","0000008c","00000090","00000094","00000098","0000009c","000000a0","000000a4","000000a8","000000ac","000000b0","000000b4","000000b8","000000bc","000000c0","000000c4","000000c8","000000cc","000000d0","000000d4","000000d8","000000dc","000000e0","000000e4","000000e8","000000ec","000000f0","000000f4","000000f8","000000fc"]
stack_memory=["00000100","00000104","00000108","0000010c","00000110","00000114","00000118","0000011c","00000120","00000124","00000128","0000012c","00000130","00000134","00000138","0000013c","00000140","00000144","00000148","0000014c","00000150","00000154","00000158","0000015c","00000160","00000164","00000168","0000016c","00000170","00000174","00000178","0000017c"]
data_emory=["00100000","00100004","00100008","0010000c","00100010","00100014","00100018","0010001c","00100020","00100024","00100028","0010002c","00100030","00100034","00100038","0010003c","00100040","00100044","00100048","0010004c","00100050","00100054","00100058","0010005c","00100060","00100064","00100068","0010006c","00100070","00100074","00100078","0010007c"]

# *******************************************************
#takes the code as input and passes it line by line 

#pc=0


def imm_to_bin(immediate, bits):
    try:
        binary = ['0'] * bits  # Initialize binary representation with all zeros

        if immediate < 0:
            # Convert negative immediate to two's complement representation
            immediate = (1 << bits) + immediate

        # Convert the immediate value to binary
        for i in range(bits - 1, -1, -1):
            binary[i] = str(immediate & 1)  # Extract least significant bit
            immediate >>= 1  # Right shift to move to the next bit
        
        return ''.join(binary)  # Convert the binary list to a string and return

    except Exception as e:
        print(f"Error: {e}")
        return None
    

# ******************************************************************************

def scan_labels(text):
    code = text.split("\n")
    for line in code:
        line=line.strip()
        inst = line.split()
        if inst=="":  # Skip empty lines
            continue

        instruction = inst[0].strip('"')
        if instruction[-1] == ':':  # Check if it's a label
            label = instruction[:-1]  # remove : from label name
            labels[label] = None      # replace None with sp when it will be added



# ******************************************************************************

def format_code(text):
    code = text.split("\n")
    output=''
    scan_labels(text)

    for line in code:
        print(line)
        line=line.strip()
        inst = line.split()
        if not inst:  # Skip empty lines
            continue
        
        
        instruction = inst[0].strip('"')  # Extract the instruction

        if instruction[-1] == ':':  # Check if it's a label
            if len(inst) == 1:
                continue
            else:
                inst = inst[1::]
                instruction=inst[0]

        if len(inst) >= 1:  # Check if there are operands present
            if '(' in inst[1] and ')' in inst[1]:
                x = inst[1].split(",")
                rd = x[0]  # Extract the destination register
                imm, rs1 = x[1].split("(")  
                rs1 = rs1.strip(')').strip('"')  
                operands = [rd, rs1, imm] 
            else:
                operands = inst[1].strip('"').split(",")  # Split the operands directly

               
                if len(operands) < 3:
                    # Pad the operands with None values if necessary
                    operands.extend([None] * (3 - len(operands)))
        else:
            operands=[]
        output=output+assembly_language(instruction, operands)+'\n'

    return output



    
# ********************************************************************************

def assembly_language(instruction, operands):

    if instruction in Rtype:
        funct3, opcode, funct7 = Rtype[instruction]

    elif instruction in Itype:
        funct3, opcode = Itype[instruction]

    elif instruction in Stype:
        funct3, opcode = Stype[instruction]

    elif instruction in Btype:
        funct3, opcode = Btype[instruction]

    elif instruction in Utype:
        opcode = Utype[instruction]

    elif instruction in Jtype:
        opcode = Jtype[instruction]

    else:
        return "Error: Instruction Not in ISA \n"

    binary_operand=[]       #to convert operands to binary 
    for op in operands:
        if op in register_address:
            binary_operand.append(register_address[op])
        else:
            binary_operand.append(op)
    
    # Rtype - add rd,rs1,rs2
    if instruction in ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]:
        rd,rs1,rs2=binary_operand
        return (funct7+rs2+rs1+funct3+rd+opcode)

    # Itype - jalr rd,rs1,imm       lw rd,imm(rs1)
    elif instruction in ["lw","addi","sltiu","jalr"]:
        rd= binary_operand[0]
        rs1= binary_operand[1]
        imm=imm_to_bin(int(binary_operand[2]),12)
        
        return (imm + rs1 + funct3 + rd + opcode)

    # Stype - sw rs2,imm(rs1)
    elif instruction=="sw":
        rs2= binary_operand[0]
        rs1= binary_operand[1]
        imm=imm_to_bin(int(binary_operand[2]),12)
        
        return (imm[0:7] + rs2 + rs1 + funct3 +imm[7:12] + opcode)

    # Btype
    elif instruction in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
        if operands == ["zero", "zero", "0"]:
        # Virtual halt instruction detected, return its binary representation
            return "0000000000000000000000000"+opcode  # Binary representation of beq zero,zero,0x00000000
    
        rs1 = binary_operand[0]
        rs2 = binary_operand[1]
        imm = imm_to_bin(int(binary_operand[2]),16)  # Assuming 12-bit immediate value

        # Extract bits from the immediate value
        immsign = imm[0]  # Bit 11
        immfirst = imm[5:11]  # Bits 4 to 1
        immlast = imm[11:]  # Bits 10 to 5

        # Encoding B-type instruction fields
        encoded_instruction = immsign + immfirst + rs2 + rs1 + funct3 + immlast + opcode

        return encoded_instruction



    # Utype - auipc rd,imm
    # Not sure if imm is 32 bit binary
    elif instruction in ["lui","auipc"]:
        rd= binary_operand[0]
        imm=imm_to_bin(int(binary_operand[1]),32)  
        return (imm[0:20] + rd + opcode)

    # Jtype - jal rd,imm
    # incorrect answer
    elif instruction=="jal":
        rd= binary_operand[0]
        imm=imm_to_bin(int(binary_operand[1]),20) 
         
        immsign=imm[0]   
        immfirst=imm[9:19]
        immlast=imm[0:9]
        
              
        return (immsign[0] + immfirst + immlast + rd + opcode )
    # + rd + opcode
    
# *****************************************************************

with open('input.txt','w') as input_file:
    input_file.write('''start: lui t0,100
    addi t1,t0,-50
    addi t2,t1,20
    add t3,t1,t2
    jal gp,-512
    jalr t4,t0,0
end: beq zero,zero,0''')


with open("input.txt", "r") as input_file, open("output.txt", "w") as output_file:
    data=input_file.read()
    formatted_output = format_code(data)  # Format the line
    output_file.write(formatted_output)  # Write the formatted line to output file

with open('output.txt','r') as output_file:
    data=output_file.read()
    print(data)
print("Conversion completed successfully.")
# print(labels)

# stack pointer
# errors
# syntax error