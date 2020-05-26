'''
Websockets installer
'''

import shutil
import subprocess
import tkinter as tk


class Result(tk.Tk):
    '''
    Install result presentation
    '''

    def __init__(self, success: bool, result: str):
        '''
        Args:
            success: True of successful
            result: installer output
        '''

        super().__init__()
        self.grid()
        self.title('Websockets installer')
        resulttext = (
            'Installation of websockets successful.' if success else
            'Installation of websockets failed!')
        self.result = tk.Label(
            self, foreground='#000000' if success else '#bb0000',
            text=resulttext)
        self.result.grid(column=0, row=0, sticky=tk.E+tk.W+tk.N)
        logmsg = []
        lines = 0
        for line in result.splitlines():
            if (not line.startswith('WARNING: You are using pip version') and
                not line.startswith('You should consider upgrading via the')):
                logmsg.append(line)
                lines += 1
                linelength = 0
                for word in line.split():
                    linelength += len(word)
                    if linelength > 80:
                        linelength = len(word) % 80
                        lines += len(word) // 80 + 1
                    if word != line.split()[-1]:
                        linelength += 1
                        if linelength > 80:
                            linelength = 1
                            lines += 1
                            break
        self.message = tk.Text(
            self, height=lines, state=tk.NORMAL, width=80, wrap=tk.WORD)
        self.message.insert('end', '\n'.join(logmsg))
        self.message.configure(state=tk.DISABLED)
        self.message.grid(column=0, row=1, sticky=tk.E+tk.W)
        self.quitbutton = tk.Button(self, text='Close', command=self.quit)
        self.quitbutton.grid(column=0, row=2, sticky=tk.S+tk.E)


def main():
    '''
    Install websockets
    '''

    pip = shutil.which('pip3')
    installer = subprocess.run(
        f'"{pip:s}" install --user --upgrade websockets',
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        text=True)
    ret = Result(installer.returncode == 0, installer.stdout)
    ret.mainloop()


if __name__ == '__main__':
    main()
