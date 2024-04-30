import clsx from 'clsx';
import s from './orderModal.module.css';
import { FC, useEffect, useRef } from 'react';
import { Modal } from 'shared/ui/modal';
import { AppButton } from 'shared/ui/appButton';
import { Link } from 'react-router-dom';
import { SubmitHandler, useForm } from 'react-hook-form';
import { InputMask } from '@react-input/mask';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Customer, Order } from 'shared/types';
import { useAdSettingsStore, useCityStore, useOrderStore } from 'shared/store';
import { useMutation } from '@tanstack/react-query';
import { postOrder } from '../api';

interface OrderModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const schema = yup
  .object({
    company_name: yup.string().max(100, 'Максимальная длина 100 символов'),
    name: yup
      .string()
      .max(100, 'Максимальная длина 100 символов')
      .matches(/^[A-Za-zА-Яа-я\s-]*$/, 'Допустимы только буквы, пробелы и дефисы')
      .required('Обязательное поле'),
    phone: yup
      .string()
      .max(18, 'Максимальная длина 18 символов')
      .matches(/^[0-9()\-\s+]*$/, 'Допустимы только цифры, скобки, пробелы и дефисы')
      .required('Обязательное поле'),
    email: yup
      .string()
      .email('Введите корректный e-mail')
      .matches(/^[A-Za-z0-9\-._@]*$/, 'Недопустимые символы. Разрешены только A-Za-z0-9.-_@')
      .max(100, 'Максимальная длина 100 символов')
  })
  .required();

const ORDER_MODAL_CONTENT_TEXT = {
  TITLE: 'Отправить на согласование',
  DESCRIPTION: 'Менеджер свяжется с вами в течение часа и проконсультирует по всем вопросам',
  BUTTON_TEXT: 'Отправить',
  DISCLAIMER: 'Нажимая на кнопку, вы даете согласие на обработку персональных данных и соглашаетесь c ',
  PRIVACY_POLICY: 'политикой конфиденциальности'
};

export const OrderModal: FC<OrderModalProps> = (props) => {
  const { isOpen, onClose } = props;
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm({
    resolver: yupResolver(schema)
  });
  const focusInputRef = useRef<HTMLInputElement | null>(null);
  const { customer_selection } = useOrderStore();
  const { adSettings, selectedRadio } = useAdSettingsStore();
  const { selectedCity } = useCityStore();
  const mutation = useMutation({
    mutationFn: postOrder
  });

  const submit: SubmitHandler<Customer> = (data) => {
    const customer = Object.fromEntries(Object.entries(data).filter(([_, value]) => value !== '')) as Customer;

    if (!selectedRadio || !adSettings.month || !adSettings.block_position || !selectedCity) return;

    const response: Order = {
      customer,
      station: selectedRadio.id,
      month: adSettings.month.id,
      block_position: adSettings.block_position.id,
      other_person_rate: adSettings.other_person_rate,
      hour_selected_rate: adSettings.hour_selected_rate,
      city: selectedCity.id,
      customer_selection
    };

    if (!response) return;

    mutation.mutate(response);
    onClose();
  };

  useEffect(() => {
    reset();
    if (isOpen && focusInputRef.current) {
      setTimeout(() => {
        focusInputRef.current!.focus();
      }, 0);
    }
  }, [isOpen]);

  return (
    <Modal hasCloseButton={true} isOpen={isOpen} onClose={onClose}>
      <div className={clsx(s.orderModal)}>
        <h3>{ORDER_MODAL_CONTENT_TEXT.TITLE}</h3>
        <p>{ORDER_MODAL_CONTENT_TEXT.DESCRIPTION}</p>
        <form className={clsx(s.orderForm)} onSubmit={handleSubmit(submit)}>
          <input
            className={clsx(errors.company_name && s.isInvalid)}
            type="text"
            placeholder={'Название организации'}
            {...register('company_name')}
          />
          <p>{errors.company_name?.message}</p>
          <input
            className={clsx(errors.name && s.isInvalid)}
            type="text"
            placeholder={'Контактное лицо*'}
            {...register('name')}
          />
          <p>{errors.name?.message}</p>
          <InputMask
            className={clsx(errors.phone && s.isInvalid)}
            type="text"
            placeholder={'Номер телефона*'}
            mask="+7 (___) ___-__-__"
            replacement={{ _: /\d/ }}
            {...register('phone')}
          />
          <p>{errors.phone?.message}</p>
          <input
            className={clsx(errors.email && s.isInvalid)}
            type="text"
            placeholder={'Электронная почта'}
            {...register('email')}
          />
          <p>{errors.email?.message}</p>
          <AppButton variant={'primary'}>{ORDER_MODAL_CONTENT_TEXT.BUTTON_TEXT}</AppButton>
        </form>
        <p>
          {ORDER_MODAL_CONTENT_TEXT.DISCLAIMER}
          <Link to={'/privacy'}>{ORDER_MODAL_CONTENT_TEXT.PRIVACY_POLICY}</Link>
        </p>
      </div>
    </Modal>
  );
};
