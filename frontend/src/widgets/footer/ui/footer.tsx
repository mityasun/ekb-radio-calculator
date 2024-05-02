import clsx from 'clsx';
import s from './footer.module.css';
import FooterLogo from 'shared/assets/logo/taksa_footer_logo.svg?react';
import { Contacts } from 'entities/contacts';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { SystemText } from 'shared/types';
import { CONTACT_TEXT_COLOR, FOOTER_PRIVACY_LINK_TEXT, FOOTER_PRIVACY_PATH } from '../configs';

export const Footer = () => {
  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });

  return (
    <footer className={clsx(s.footer)}>
      <div className={clsx(s.footerWrapper)}>
        <div className={clsx(s.footerContacts)}>
          <FooterLogo className={clsx(s.footerIcon)} />
          <Contacts textColor={CONTACT_TEXT_COLOR.WHITE} variant={'primary'} />
        </div>
        <div className={clsx(s.footerPoliticy)}>
          <Link className={clsx(s.footerLinkPoliticy)} to={FOOTER_PRIVACY_PATH}>
            {FOOTER_PRIVACY_LINK_TEXT}
          </Link>
          {systemText?.copyright && <p>{systemText.copyright}</p>}
        </div>
      </div>
    </footer>
  );
};
