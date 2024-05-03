import clsx from 'clsx';
import s from './privacyPage.module.css';
import { useQuery } from '@tanstack/react-query';
import { Helmet } from 'react-helmet-async';
import { SystemText } from 'shared/types';
import { PRIVACY_PAGE_CONTENT_TEXT } from '../configs';
import { useEffect } from 'react';

export const PrivacyPage = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });
  const markup = { __html: systemText?.privacy_text ? systemText.privacy_text : '' };

  return (
    <div className={clsx(s.privacyPage)}>
      <>
        <Helmet>
          <title>
            {PRIVACY_PAGE_CONTENT_TEXT.TITLE +
              (systemText?.title && PRIVACY_PAGE_CONTENT_TEXT.TITLE_SEPARATOR + systemText.title)}
          </title>
        </Helmet>
        <h2>Политика конфиденциальности</h2>
        <article dangerouslySetInnerHTML={markup} />
      </>
    </div>
  );
};
