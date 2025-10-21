public class taller_java {
    public static void main(String[] args) {
        // 1. Crear una variable tipo String nombre y almacenar sus nombres
        String nombre = "Angel";
        
        // 2. Crear una variable tipo String apellido y poner sus apellidos
        String apellido = "Arias";
        
        // 3. Crear una variable tipo char y almacenar la primera letra de su nombre
        char primeraLetra = 'A';
        
        // 4. Imprimir Mi nombre es nombre, apellido
        System.out.println("Mi nombre es " + nombre + ", " + apellido);
        
        // 5. Crear una variable tipo int edad y almacenar la edad
        int edad = 18;
        
        // 6. Crear una variable tipo flotante y almacenar la estatura
        float estatura = 1.75f;
        
        // 7. Imprimir Tengo edad años y mido estatura metros.
        System.out.println("Tengo " + edad + " años y mido " + estatura + " metros. La primera letra de mi nombre es " + primeraLetra);
        
        // 8. Crear una variable tipo booleano que almacene si eres o no mayor de edad
        // (true si eres mayor de edad, false si eres menor de edad)
        boolean mayorDeEdad = (edad >= 18);
        
        // 9. Si la variable=true que imprima que eres mayor de edad, 
        // de lo contrario, que eres menor de edad
        if (mayorDeEdad) {
            System.out.println("Eres mayor de edad");
        } else {
            System.out.println("Eres menor de edad");
        }
        
        // 10. Imprimir "Eso es todo amigos"
        System.out.println("Eso es todo amigos");
    }
}