import clsx from 'clsx';
import s from './contacts.module.css';
import PhoneIcon from 'shared/assets/icon/Calling.svg?react';
import EmailIcon from 'shared/assets/icon/Message.svg?react';
import AddressIcon from 'shared/assets/icon/Map_point.svg?react';
import { FC } from 'react';
import { useQuery } from '@tanstack/react-query';
import { SystemText } from 'shared/types';
import { LINK_ORG_YANDEX_MAP } from '../configs';

interface ContactsProps {
  textColor: string;
  variant: 'primary' | 'header';
}

export const Contacts: FC<ContactsProps> = (props) => {
  const { textColor, variant = 'primary' } = props;
  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });

  const phoneTextToLink = systemText?.phone
    ? `tel:+${systemText?.phone
        .split('')
        .filter((item) => Number(item))
        .join('')}`
    : '';

  const getCity = () => {
    if (!systemText?.address) return;
    return systemText?.address.split(',').map((item) => {
      if (item.includes('г.')) return item;
    });
  };

  const getAddress = () => {
    if (!systemText?.address) return;

    return systemText.address
      .split(',')
      .filter((item) => {
        if (!item.includes('г.')) return item;
      })
      .join(', ');
  };

  return (
    <div className={clsx(s.contacts)}>
      {systemText && (
        <>
          <ul className={clsx(s.contactsList)}>
            <li className={clsx(s.contactsListItem)}>
              <a
                className={clsx(s.contactsListLink)}
                href={phoneTextToLink}
                style={{ color: textColor }}
                target="_blank"
                rel="noreferrer">
                <PhoneIcon />
                <span className={clsx(variant === 'header' && s.addressHeader)}>{systemText.phone}</span>
              </a>
            </li>
            <li className={clsx(s.contactsListItem)}>
              <a
                className={clsx(s.contactsListLink)}
                href={`mailto:${systemText.email}`}
                style={{ color: textColor }}
                target="_blank"
                rel="noreferrer">
                <EmailIcon />
                <span className={clsx(variant === 'header' && s.addressHeader)}>{systemText.email}</span>
              </a>
            </li>
          </ul>
          <div className={clsx(s.address, variant === 'header' && s.addressHeader)}>
            <a href={LINK_ORG_YANDEX_MAP} target="_blank" rel="noreferrer">
              <AddressIcon />
            </a>
            <div>
              <p style={{ color: textColor }}>{getCity()}</p>
              <p style={{ color: textColor }}>{getAddress()}</p>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
