import clsx from 'clsx';
import s from './radioStationDescription.module.css';
import { useAdSettingsStore } from 'shared/store';

const LOGO_IMG_ALT = 'Логотип радиостанции';
const NO_SATATION_TEXT = 'В этом городе выбор радиостанции пока не доступен!';

export const RadioStationDescription = () => {
  const { selectedRadio } = useAdSettingsStore();
  const markup = { __html: selectedRadio?.description ? selectedRadio?.description : '' };

  return (
    <div className={clsx(s.radioStationDescription)}>
      {selectedRadio && (
        <>
          <div className={clsx(s.radioStationDescriptionText)}>
            <h3>{selectedRadio.title}</h3>
            <img src={selectedRadio.logo} alt={LOGO_IMG_ALT} />
            <p dangerouslySetInnerHTML={markup}></p>
          </div>
        </>
      )}
      {!selectedRadio && <h4>{NO_SATATION_TEXT}</h4>}
    </div>
  );
};
