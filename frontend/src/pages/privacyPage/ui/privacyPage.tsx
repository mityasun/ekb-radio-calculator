import clsx from 'clsx';
import s from './privacyPage.module.css';
import { useQuery } from '@tanstack/react-query';
import { Helmet } from 'react-helmet-async';
import { SystemText } from 'shared/types';

export const PrivacyPage = () => {
  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });
  const markup = { __html: systemText?.privacy_text ? systemText.privacy_text : '' };

  return (
    <div className={clsx(s.privacyPage)}>
      <>
        <Helmet>
          <title>{`Политика конфиденциальности и условия обработки персональных данных
          ${systemText?.title && ' | ' + systemText.title}`}</title>
        </Helmet>
        <h2>Политика конфиденциальности</h2>
        <article dangerouslySetInnerHTML={markup} />
      </>
    </div>
  );
};
