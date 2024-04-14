import clsx from 'clsx';
import s from './footer.module.css';
import FooterLogo from 'shared/assets/logo/taksa_footer_logo.svg?react';

export const Footer = () => {
  return (
    <footer className={clsx(s.footer)}>
      <div className={clsx(s.footerWrapper)}>
        <FooterLogo />
      </div>
    </footer>
  );
};
