import clsx from 'clsx';
import s from './adSettingsSelector.module.css';
import { AdDurationSelector } from 'entities/adDurationSelector';
import { AdMonthSelector } from 'entities/adMonthSelector';
import { AdPositionSelector } from 'entities/adPositionSelector';
import Switch from 'react-switch';
import { useAdSettingsStore } from 'shared/store';

const SELECT_DURATION_LABEL = 'Длительность ролика';
const SELECT_POSITION_LABEL = 'Позиционирование в рекламном блоке';
const SELECT_MONTH_LABEL = 'Месяц размешения';
const SWITCH_GUARANTEED_HOUR_LABEL = 'Гарантированный выбор часа';
const SWITCH_THIRD_PARTY_LABEL = 'Упоминание 3-их лиц';
const onColor = '#05bb75';

export const AdSettingsSelector = () => {
  const { adSettings, setHourSelection, setOtherPerson } = useAdSettingsStore();

  const handleHourSelectionChange = (value: boolean) => {
    setHourSelection(value);
  };

  const handleOtherPersonChange = (value: boolean) => {
    setOtherPerson(value);
  };

  return (
    <div className={clsx(s.adSettings)}>
      <div className={clsx(s.adSettingsSelector)}>
        <div>
          <p>{SELECT_DURATION_LABEL}</p>
          <AdDurationSelector />
        </div>
        <div>
          <p>{SELECT_POSITION_LABEL}</p>
          <AdPositionSelector />
        </div>
        <div>
          <p>{SELECT_MONTH_LABEL}</p>
          <AdMonthSelector />
        </div>
      </div>
      <div className={clsx(s.adSettingsSwitch)}>
        <div>
          <p>{SWITCH_GUARANTEED_HOUR_LABEL}</p>
          <Switch
            onChange={handleHourSelectionChange}
            checked={adSettings.hour_selected_rate || false}
            uncheckedIcon={false}
            checkedIcon={false}
            onColor={onColor}
            activeBoxShadow="none"
          />
        </div>
        <div>
          <p>{SWITCH_THIRD_PARTY_LABEL}</p>
          <Switch
            onChange={handleOtherPersonChange}
            checked={adSettings.other_person_rate || false}
            uncheckedIcon={false}
            checkedIcon={false}
            onColor={onColor}
            activeBoxShadow="none"
          />
        </div>
      </div>
    </div>
  );
};
