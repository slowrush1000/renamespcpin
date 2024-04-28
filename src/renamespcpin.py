
import sys

class Renamepinspc:
    def __init__(self):
        self.m_input_filename   = ''
        self.m_output_filename  = ''
        self.m_pin_prefix       = 'p'
        self.m_pin_dic          = {}     # key : org_pin, data : new_pin
        self.m_pin_count        = 1
    def SetInputFilename(self, input_filename):
        self.m_input_filename   = input_filename
    def GetInputFilename(self):
        return self.m_input_filename
    def SetOutputFilename(self, output_filename):
        self.m_output_filename = output_filename
    def GetOutputFilename(self):
        return self.m_output_filename
    def SetpinPrefix(self, pin_prefix):
        self.m_pin_prefix = pin_prefix
    def GetpinPrefix(self):
        return self.m_pin_prefix
    def Addpin(self, org_pin, new_pin):
        if not org_pin in self.m_pin_dic:
            self.m_pin_dic[org_pin]   = new_pin
    def GetNewpin(self, org_pin):
        if org_pin in self.m_pin_dic:
            return self.m_pin_dic[org_pin]
        else:
            return str('*')
    def MakeNewpin(self):
        new_pin = f'{self.m_pin_prefix}_{self.m_pin_count}'
        self.m_pin_count += 1
        return new_pin
    def PrintUsage(self):
        print(f'renamepinspc.py usage:')
        print(f'python3 renamepinspc.py input_file output_file')
    def ReadArgs(self, args):
        if 3 != len(args):
            self.PrintUsage()
            exit()
        self.SetInputFilename(args[1])
        self.SetOutputFilename(args[2])
    def PrintInput(self):
        print(f'# print input start')
        print(f'    input file  : {self.GetInputFilename()}')
        print(f'    output file : {self.GetOutputFilename()}')
        print(f'# print input end')
    def ReadWriteFile(self):
        print(f'# read/write start')
        input_file  = open(self.GetInputFilename(), 'rt')
        output_file = open(self.GetOutputFilename(), 'wt')
        total_lines = []
        while True:
            line = input_file.readline()
            if not line:
                break
            line    = line.lstrip().rstrip()
            if 0 == len(line):
                continue
            if '+' == line[0]:
                total_lines.append(line[1:])
            else:
                new_total_line  = self.ReadTotalLine(' '.join(total_lines))
                output_file.write(f'{new_total_line}\n')
                total_lines     = []
                total_lines.append(line)
        new_total_line  = self.ReadTotalLine(' '.join(total_lines))
        output_file.write(f'{new_total_line}\n')
        input_file.close()
        output_file.close()
        print(f'# read/write end')
    def ReadTotalLine(self, total_line):
        print(f'total_line : {total_line}')
        new_total_line  = ''
        tokens  = total_line.split()
        if 0 == len(tokens):
            return ''
        if '.subckt' == tokens[0]:
            new_total_line  = f'.subckt {tokens[1]} '
            #
            for pos in range(2, len(tokens)):
                org_pin    = tokens[pos]
                new_pin    = self.MakeNewpin()
                print(f'{org_pin} > {new_pin}')
                if '*' == self.GetNewpin(org_pin):
                    self.Addpin(org_pin, new_pin)
                new_total_line  = f'{new_total_line}\n+ {new_pin}'
            #
        elif '.ends' == tokens[0]:
            for token in tokens:
                new_total_line  = total_line
        else:
            for token in tokens:
                new_pin     = self.GetNewpin(token)
                if '*' != new_pin:
                    if 0 == len(new_total_line):
                        new_total_line  = new_pin
                    else:
                        new_total_line  = f'{new_total_line} {new_pin}'
                else:
                    if 0 == len(new_total_line):
                        new_total_line  = token
                    else:
                        new_total_line  = f'{new_total_line} {token}'
        return new_total_line
    def Run(self, args):
        print(f'# renamespcpin.py start')
        self.ReadArgs(args)
        self.PrintInput()
        self.ReadWriteFile()
        print(f'# renamespcpin.py end')

def main(args):
    my_renamespcpin    = Renamepinspc()
    my_renamespcpin.Run(args)
#    test_args           = [ 'renamespcpin.py', 'tests/test.spc', 'tests/test.out.spc']
#    my_renamespcpin.Run(test_args)

if __name__ == '__main__':
    main(sys.argv)