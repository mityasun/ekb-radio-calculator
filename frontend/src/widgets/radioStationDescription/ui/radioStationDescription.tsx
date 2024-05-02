import clsx from 'clsx';
import s from './radioStationDescription.module.css';
import { useStore } from 'shared/store';
import { LOGO_IMG_ALT, NO_SATATION_TEXT } from '../configs';

export const RadioStationDescription = () => {
  const { selectedRadio } = useStore();
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
