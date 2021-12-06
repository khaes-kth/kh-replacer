import sys

def main(argv):
    dir = argv[0]
    mod = int(argv[1])
    for i in range(0, mod):
        with open(f'{dir}/Main{i}.java', 'w') as f:
            f.write(f'''
                import java.util.Arrays;
                public class Main{i}''' + '''{
                    public static void main(String[] args){
                        String[] arr = new String[] {
                ''')

            for j in range(0, mod):
                curNumber = i * mod + j
                f.write(f'"T{curNumber}T",')

            lastNumber = mod * (i + 1)
            f.write(f'"T{lastNumber}T"' + '}; Arrays.asList(arr).forEach(System.out::println);} }')

if __name__ == "__main__":
    main(sys.argv[1:])
