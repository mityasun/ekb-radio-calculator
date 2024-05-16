import clsx from 'clsx';
import style from './fallback.module.css';
import { FALLBACK_CONTENT_TEXT } from '../configs';

export const Fallback = ({ error }: { error: { message: string } }) => {
  console.log(error);
  return (
    <div role="alert" className={clsx(style.fallback)}>
      <h1 className={clsx(style.fallbackTitle)}>{FALLBACK_CONTENT_TEXT.TITLE}</h1>
      <p className={clsx(style.fallbackDescribe, style.fallbackDescribeError)}>{`Ошибка: ${error.message}`}</p>
      <p className={clsx(style.fallbackDescribe)}>
        {FALLBACK_CONTENT_TEXT.MESSAGE}
        <a className={clsx(style.fallbackLink)} href="mailto:hello@ekb-radio.ru">
          {FALLBACK_CONTENT_TEXT.LINK_TEXT}
        </a>
      </p>
    </div>
  );
};
