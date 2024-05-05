import * as yup from 'yup';

export const SCHEMA_VALIDATION = yup
  .object({
    company_name: yup.string().max(100, 'Максимальная длина 100 символов'),
    name: yup
      .string()
      .max(100, 'Максимальная длина 100 символов')
      .matches(/^[A-Za-zА-Яа-я\s-]*$/, 'Допустимы только буквы, пробелы и дефисы')
      .required('Обязательное поле'),
    phone: yup
      .string()
      .min(11, 'Минимальная длина 11 символов')
      .max(18, 'Максимальная длина 18 символов')
      .matches(/^[0-9()\-\s+]*$/, 'Допустимы только цифры, скобки, пробелы и дефисы')
      .required('Обязательное поле'),
    email: yup
      .string()
      .email('Введите корректный e-mail')
      .matches(/^[A-Za-z0-9\-._@]*$/, 'Недопустимые символы. Разрешены только A-Za-z0-9.-_@')
      .max(100, 'Максимальная длина 100 символов')
      .test(
        'optional-email',
        'Минимальная длина 6 символов',
        (value) => !value || (typeof value === 'string' && value.length >= 6)
      )
  })
  .required();

export const ORDER_MODAL_CONTENT_TEXT = {
  TITLE: 'Отправить на согласование',
  DESCRIPTION: 'Менеджер свяжется с вами в течение часа и проконсультирует по всем вопросам',
  BUTTON_TEXT: 'Отправить',
  DISCLAIMER: 'Нажимая на кнопку, вы даете согласие на обработку персональных данных и соглашаетесь c ',
  PRIVACY_POLICY: 'политикой конфиденциальности',
  SUCCESS: 'Ваша заявка отправлена, мы свяжемся с вами для подтверждения заявки',
  FORM_PLACEHOLDER_COMPANY_NAME: 'Название организации',
  FORM_PLACEHOLDER_NAME: 'Контактное лицо*',
  FORM_PLACEHOLDER_PHONE: 'Номер телефона*',
  FORM_PLACEHOLDER_EMAIL: 'Электронная почта'
};

export const PHONE_MASK = '+7 (___) ___-__-__';
