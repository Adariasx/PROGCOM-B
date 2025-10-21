public class taller_java {
    public static void main(String[] args) {
        //Crear una variable tipo String nombre y almacenar sus nombres
        String nombre = "Angel";
        
        //Crear una variable tipo String apellido y poner sus apellidos
        String apellido = "Arias";
        
        //Crear una variable tipo char y almacenar la primera letra de su nombre
        char primeraLetra = 'A';
        
        //Imprimir Mi nombre es nombre, apellido
        System.out.println("Mi nombre es " + nombre + ", " + apellido);
        
        //Crear una variable tipo int edad y almacenar la edad
        int edad = 18;
        
        //Crear una variable tipo flotante y almacenar la estatura
        float estatura = 1.75f;
        
        //Imprimir Tengo edad años y mido estatura metros.
        System.out.println("Tengo " + edad + " años y mido " + estatura + " metros. La primera letra de mi nombre es " + primeraLetra);
        
        //Crear una variable tipo booleano que almacene si eres o no mayor de edad
        boolean mayorDeEdad = (edad >= 18);
        
        //Verficiar si eres mayor de edad o menor de edad y dar un print
        if (mayorDeEdad) {
            System.out.println("Eres mayor de edad");
        } else {
            System.out.println("Eres menor de edad");
        }
        
        //ejercicio muy facil
        System.out.println("Eso es todo amigos");
    }
}