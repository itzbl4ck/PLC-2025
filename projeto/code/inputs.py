input_teste = """ program Main; 
             { 
                meu programa 
                alo
             }
             // ola

             (* kkahds *)

             var 
                x,i : integer;
             begin
                begin
                begin
                    x := 0; 
                    for i := 5 downto 1 do 
                    begin
                        x := x+i
                    end
                end
                end
             end.
    """

input_fun = """
program CalculaDobro;

function Dobro(x: integer): integer;
begin
  Dobro := x * 2;
end;

function Soma(x,y :integer): integer;
var
    a : integer;
begin
    Soma := x + y;
end;

var
  resultado: integer;
begin
  resultado := Dobro(Soma(1,3));
end.
"""

input_fun2 = """
program CalculaDobro;
function Soma(x,y :integer): integer;
begin
  Soma := x + y;
end;

var
  resultado: integer;
begin
  resultado := Soma(3, 9);
end.
"""

input_fac = """
program factorial;
function Factorial(x :integer): integer;
begin 
    if x = 0 then
    Factorial := 1
    else 
    Factorial := Factorial(x-1) * x;
end;
var resultado : integer;

begin
    resultado := 99;
    resultado := Factorial(9);
end.
"""

input_1 = """
            program HelloWorld;
            begin
                writeln('Ola, Mundo!');
            end.
"""



input_2 = """
    program Fatorial;
    var
    n, i, fat: integer;
    begin
    writeln('Introduza um número inteiro positivo:');
    readln(n);
    fat := 1;
    for i := 1 to n do
    fat := fat * i;
    writeln('Fatorial de ', n, ': ', fat);
    end.
"""


input_3 = """
    program NumeroPrimo;
    var
    num, i: integer;
    primo: boolean;
    begin
    writeln('Introduza um número inteiro positivo:');
    readln(num);
    primo := true;
    i := 2;
    while (i <= (num div 2)) and primo do
    begin
    if (num mod i) = 0 then
    primo := false;
    i := i + 1;
    end;
    if primo then
    writeln(num, ' é um número primo')
    else
    writeln(num, ' não é um número primo')
    end.
"""

input_4 = """
program SomaArray;
var
numeros: array[1..5] of integer;
i, soma: integer;
begin
soma := 0;
writeln('Introduza 5 números inteiros:');
for i := 1 to 5 do
begin
readln(numeros[i]);
soma := soma + numeros[i];
end;
writeln('A soma dos números é: ', soma);
end.
"""


input_5 = """
program BinarioParaInteiro;

function BinToInt(bin: string): integer;
var
  i, valor, potencia: integer;
begin
  valor := 0;
  potencia := 1;

  for i := length(bin) downto 1 do
  begin
    if bin[i] = '1' then
      valor := valor + potencia;
    potencia := potencia * 2;
  end;

  BinToInt := valor;
end;

var
  bin: string;
  valor: integer;
begin
  writeln('Introduza uma string binária:');
  readln(bin);
  valor := BinToInt(bin);
  writeln('O valor inteiro correspondente é: ', valor);
end.

"""



input_6 = """
program OperacoesComNumeros;

{ Função que calcula o quadrado de um número }
function Quadrado(x: integer): integer;
begin
    Quadrado := x * x;
end;

{ Função que calcula a soma de dois números }
function Soma(a, b: integer): integer;
begin
    Soma := a + b;
end;

{ Função que devolve o maior de dois números }
function Maximo(a, b: integer; c : boolean): integer;
begin
    if a > b then
        Maximo := a
    else
        Maximo := b;
end;

var
    x, y, r1, r2, r3: integer;

begin
    writeln('Introduza dois inteiros:');
    readln(x, y);

    r1 := Quadrado(x);
    r2 := Soma(x, y);
    r3 := Maximo(x, y);

    writeln('Quadrado de ', x, ': ', r1);
    writeln('Soma de ', x, ' e ', y, ': ', r2);
    writeln('Máximo entre ', x, ' e ', y, ': ', r3);
end.

"""

input_7 = """
program SomaMatriz;
var
    matriz: array[1..3, 1..3] of integer;
    i, j: integer;
    soma: integer;
begin
    soma := 0;
    { Ler valores para a matriz }
    for i := 1 to 3 do
    begin
        for j := 1 to 3 do
        begin
            readln(matriz[i, j]);
        end;
    end;
    { Somar todos os elementos }
    for i := 1 to 3 do
    begin
        for j := 1 to 3 do
        begin
            soma := soma + matriz[i, j];
        end;
    end;
    { Escrever o resultado }
    writeln(soma);
end.
"""

input_8 = """
program OperacoesComNumeros;


var
    x, y, r1, r2, r3: integer;
    r4 : boolean;
begin

    r2 := 3;



    if r1 = 2 then
        begin
        r1 := 1;
        
        r4 := false;

        if r1 = 3 then
        begin
        r2 := 3
        end;

        end;
    r3 := 3
end.


"""


input_bool = """
program ExemploBooleano;

function AmbosVerdadeiros(a, b: boolean): boolean;
begin
  AmbosVerdadeiros := a and b;
end;

var
  x, y: boolean;
begin
  x := true;
  y := true;

  if AmbosVerdadeiros(x, y) then
    writeln('Os dois sao verdadeiros')
  else
    writeln('Pelo menos um e falso');
end.
"""