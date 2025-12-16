import { z } from 'zod';

export const signupSchema = z.object({
    username: z
        .string()
        .min(3, "Le nom d'utilisateur doit contenir au moins 3 caractères")
        .max(20, "Le nom d'utilisateur est trop long"),

    email: z
        .string()
        .email("Format d'email invalide"),

    phone_number: z
        .string()
        .min(10, "Le numéro de téléphone doit contenir au moins 10 chiffres")
        .max(15, "Le numéro de téléphone est trop long"),

    password: z
        .string()
        .min(8, "Le mot de passe doit faire au moins 8 caractères")
        .regex(/[A-Z]/, "Il faut au moins une majuscule")
        .regex(/[0-9]/, "Il faut au moins un chiffre"),

    confirm_password: z
        .string()
        .min(1, "La confirmation est requise"),
})

    .refine((data) => data.password === data.confirm_password, {
        message: "Les mots de passe ne correspondent pas",
        path: ["confirm_password"], 
    });