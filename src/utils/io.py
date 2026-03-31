import io

def change_label_number():

    with open('C:/Users/697/projecten/labeling/data/labels/fb437a33-021-1.txt') as topo_file:
        for line in topo_file:
            # print(line.split(" ")[0])
            # print(line[0]),
            match line.split(" ")[0]:
                case "0":
                    print(f"0 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "1":
                    print(f"1 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "4":
                    print(f"2 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "5":
                    print(f"3 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "16":
                    print(f"4 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "17":
                    print(f"5 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "18":
                    print(f"6 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "19":
                    print(f"7 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "20":
                    print(f"8 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "21":
                    print(f"9 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="") 
                case "22":
                    print(f"10 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "23":
                    print(f"11 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "24":
                    print(f"12 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "30":
                    print(f"13 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")
                case "31":
                    print(f"14 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]}", end="")

   
        

def change_label_number2():

    with open("C:/Users/697/projecten/labeling/more data/data/labels/fb437a33-021-1.txt") as topo_file:
        for line in topo_file:
            # print(line.split(" ")[0])
            # print(line[0]),
            match line.split(" ")[0]:
                case "0":
                    print(f"0 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "1":
                    print(f"1 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "4":
                    print(f"2 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "5":
                    print(f"3 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "16":
                    print(f"4 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "17":
                    print(f"5 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "18":
                    print(f"6 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "19":
                    print(f"7 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "20":
                    print(f"8 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "21":
                    print(f"9 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="") 
                case "22":
                    print(f"10 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "23":
                    print(f"11 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "24":
                    print(f"12 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "30":
                    print(f"13 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")
                case "31":
                    print(f"14 {line.split(" ")[1]} {line.split(" ")[2]} {line.split(" ")[3]} {line.split(" ")[4]} {line.split(" ")[5]} {line.split(" ")[6]} {line.split(" ")[7]} {line.split(" ")[8]}", end="")


change_label_number2()