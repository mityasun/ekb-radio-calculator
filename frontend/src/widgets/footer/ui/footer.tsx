import clsx from 'clsx';
import s from './footer.module.css';
import FooterLogo from 'shared/assets/logo/taksa_footer_logo.svg?react';
import { Contacts } from 'shared/ui/contacts';
import { Link } from 'react-router-dom';

export const Footer = () => {
  return (
    <footer className={clsx(s.footer)}>
      <div className={clsx(s.footerWrapper)}>
        <FooterLogo className={clsx(s.footerIcon)} />
        <Contacts textColor={'#ffffff'} variant={'primary'} />
      </div>
      <Link to="/privacy">Privacy</Link>
    </footer>
  );
};
