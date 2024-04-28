import clsx from 'clsx';
import s from './footer.module.css';
import FooterLogo from 'shared/assets/logo/taksa_footer_logo.svg?react';
import { Contacts } from 'entities/contacts';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { SystemText } from 'shared/types';

const FOOTER_PRIVACY_LINK = '/privacy';
const FOOTER_PRIVACY_LINK_TEXT = 'Политика конфиденциальности';

export const Footer = () => {
  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });

  return (
    <footer className={clsx(s.footer)}>
      <div className={clsx(s.footerWrapper)}>
        <div className={clsx(s.footerContacts)}>
          <FooterLogo className={clsx(s.footerIcon)} />
          <Contacts textColor={'#ffffff'} variant={'primary'} />
        </div>
        <div className={clsx(s.footerPoliticy)}>
          <Link className={clsx(s.footerLinkPoliticy)} to={FOOTER_PRIVACY_LINK}>
            {FOOTER_PRIVACY_LINK_TEXT}
          </Link>
          {systemText?.copyright && <p>{systemText.copyright}</p>}
        </div>
      </div>
    </footer>
  );
};
