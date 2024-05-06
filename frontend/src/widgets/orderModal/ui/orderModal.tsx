import clsx from 'clsx';
import s from './orderModal.module.css';
import { FC, useEffect, useRef } from 'react';
import { Modal } from 'shared/ui/modal';
import { AppButton } from 'shared/ui/appButton';
import { Link } from 'react-router-dom';
import { SubmitHandler, useForm } from 'react-hook-form';
import { InputMask } from '@react-input/mask';
import { yupResolver } from '@hookform/resolvers/yup';
import { Customer } from 'shared/types';
import { useStore } from 'shared/store';
import { useMutation } from '@tanstack/react-query';
import { postOrder } from '../api';
import { ORDER_MODAL_CONTENT_TEXT, PHONE_MASK, SCHEMA_VALIDATION } from '../configs';
import { submitOrder } from '../utils';

interface OrderModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const OrderModal: FC<OrderModalProps> = (props) => {
  const { isOpen, onClose } = props;
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm({
    resolver: yupResolver(SCHEMA_VALIDATION)
  });
  const focusInputRef = useRef<HTMLInputElement | null>(null);
  const { appSettings, selectedRadio, selectedCity, customer_selection } = useStore();
  const mutation = useMutation({
    mutationFn: postOrder
  });

  const submit: SubmitHandler<Customer> = (data) => {
    submitOrder(data, customer_selection, selectedCity, selectedRadio, appSettings, mutation);
  };

  useEffect(() => {
    if (mutation.isSuccess || mutation.isError) {
      mutation.reset();
    }

    reset();
    if (isOpen && focusInputRef.current) {
      setTimeout(() => {
        focusInputRef.current!.focus();
      }, 0);
    }
  }, [isOpen]);

  useEffect(() => {
    if (mutation.isSuccess) {
      setTimeout(onClose, 3000);
    }
  }, [mutation.isSuccess]);

  return (
    <Modal hasCloseButton={true} isOpen={isOpen} onClose={onClose}>
      <div className={clsx(s.orderModal)}>
        <h3>{ORDER_MODAL_CONTENT_TEXT.TITLE}</h3>
        {!mutation.isSuccess && (
          <>
            <p>{ORDER_MODAL_CONTENT_TEXT.DESCRIPTION}</p>
            <form className={clsx(s.orderForm)} onSubmit={handleSubmit(submit)}>
              <input
                className={clsx(errors.company_name && s.isInvalid)}
                type="text"
                placeholder={ORDER_MODAL_CONTENT_TEXT.FORM_PLACEHOLDER_COMPANY_NAME}
                {...register('company_name')}
              />
              <p>{errors.company_name?.message}</p>
              <input
                className={clsx(errors.name && s.isInvalid)}
                type="text"
                placeholder={ORDER_MODAL_CONTENT_TEXT.FORM_PLACEHOLDER_NAME}
                {...register('name')}
              />
              <p>{errors.name?.message}</p>
              <InputMask
                className={clsx(errors.phone && s.isInvalid)}
                type="text"
                placeholder={ORDER_MODAL_CONTENT_TEXT.FORM_PLACEHOLDER_PHONE}
                mask={PHONE_MASK}
                replacement={{ _: /\d/ }}
                {...register('phone')}
              />
              <p>{errors.phone?.message}</p>
              <input
                className={clsx(errors.email && s.isInvalid)}
                type="text"
                placeholder={ORDER_MODAL_CONTENT_TEXT.FORM_PLACEHOLDER_EMAIL}
                {...register('email')}
              />
              <p>{errors.email?.message}</p>
              <AppButton variant={'primary'} disabled={mutation.isPending}>
                {mutation.isPending
                  ? ORDER_MODAL_CONTENT_TEXT.BUTTON_TEXT_IS_PANDING
                  : ORDER_MODAL_CONTENT_TEXT.BUTTON_TEXT}
              </AppButton>
            </form>
          </>
        )}
        {mutation.isSuccess && <h4 className={clsx(s.isSuccess)}>{ORDER_MODAL_CONTENT_TEXT.SUCCESS}</h4>}
        {mutation.isError && <h4 className={clsx(s.isError)}>{mutation.error.message}</h4>}
        <p>
          {ORDER_MODAL_CONTENT_TEXT.DISCLAIMER}
          <Link to={'/privacy'}>{ORDER_MODAL_CONTENT_TEXT.PRIVACY_POLICY}</Link>
        </p>
      </div>
    </Modal>
  );
};
