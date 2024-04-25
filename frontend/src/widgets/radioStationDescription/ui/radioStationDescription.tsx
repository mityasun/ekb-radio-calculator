import clsx from 'clsx';
import s from './radioStationDescription.module.css';
import { useRadioStore } from 'shared/store';

const logoImgAlt = 'Логотип радиостанции';

export const RadioStationDescription = () => {
  const { selectedRadio } = useRadioStore();

  if (!selectedRadio) {
    return <p style={{ fontSize: '1.6rem', textAlign: 'center', margin: '20px auto' }}>Loading ...</p>;
  }

  return (
    <div className={clsx(s.radioStationDescription)}>
      <div className={clsx(s.radioStationLogo)}>
        <img src={selectedRadio.logo} alt={logoImgAlt} />
      </div>
      <div className={clsx(s.radioStationDescriptionText)}>
        <h3>{selectedRadio.title}</h3>
        <article>{selectedRadio.description}</article>
      </div>
    </div>
  );
};
