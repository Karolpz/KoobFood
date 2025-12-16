import React from 'react'
import InputField from '../../components/Form/InputField/InputField'
import { signupUser } from '../../api/apiUser'
import Button from '../../components/Button/Button'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { signupSchema } from '../../components/Form/formSchema'
import { useNavigate } from 'react-router-dom'

const Signup = () => {

  const navigate = useNavigate()
  
    const {
      register,
      handleSubmit,
      formState: { errors, isSubmitting }
    } = useForm({
      resolver: zodResolver(signupSchema)
    });

    const onSubmit = async (data) => {
      try {
        console.log(data)
        const response = await signupUser(data)
        console.log('User signed up successfully:', response)
        navigate('/login')
      } catch (error) {
        console.error('Error signing up user:', error)
      }
    }

    return (
      <section className='signup'>
        <h2 className='signup__title'>Inscription</h2>
        <form method='POST' className='signup__form' onSubmit={handleSubmit(onSubmit)}>

          <InputField
            label="Nom d'utilisateur"
            id="username"
            name="username"
            register={register}
            error={errors.username}
          />

          <InputField
            label="Email"
            type="email"
            id="email"
            name="email"
            register={register}
            error={errors.email}
          />

          <InputField
            label="Numéro de téléphone"
            id="phone_number"
            name="phone_number"
            register={register}
            error={errors.phone_number}
          />

          <InputField
            label="Mot de passe"
            type="password"
            id="password"
            name="password"
            register={register}
            error={errors.password}
            autocomplete="new-password"
          />

          <InputField
            label="Confirmer le mot de passe"
            type="password"
            id="confirm_password"
            name="confirm_password"
            register={register}
            error={errors.confirm_password}
            autocomplete="new-password"
          />

          <Button
            text={isSubmitting ? "Inscription..." : "S'inscrire"}
            type="submit"
            className="signup__button"
            disabled={isSubmitting}
          />
        </form>
      </section>
    )
  }

export default Signup