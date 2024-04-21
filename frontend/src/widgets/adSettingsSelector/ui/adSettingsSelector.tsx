import clsx from 'clsx';
import s from './adSettingsSelector.module.css';
import { AdDurationSelector } from 'entities/adDurationSelector';
import { AdMonthSelector } from 'entities/adMonthSelector';
import { AdPositionSelector } from 'entities/adPositionSelector';
import { useCallback, useEffect, useState } from 'react';
import Switch from 'react-switch';

const SELECT_DURATION_LABEL = 'Длительность ролика';
const SELECT_POSITION_LABEL = 'Позиционирование в рекламном блоке';
const SELECT_MOUNTH_LABEL = 'Месяц размешения';
const SWITCH_GUARANTEED_HOUR_LABEL = 'Гарантированный выбор часа';
const SWITCH_THIRD_PARTY_LABEL = 'Упоминание 3-их лиц';
const onColor = '#05bb75';

export const AdSettingsSelector = () => {
  const [selectedAdSettings, setSelectedAdSettings] = useState({
    audio_duration: '',
    block_position: '',
    month: '',
    guaranteed_hour: false,
    third_party: false
  });

  const handleDurationChange = useCallback((value: string) => {
    setSelectedAdSettings((prevSettings) => ({
      ...prevSettings,
      audio_duration: value
    }));
  }, []);

  const handlePositionChange = useCallback((value: string) => {
    setSelectedAdSettings((prevSettings) => ({
      ...prevSettings,
      block_position: value
    }));
  }, []);

  const handleMonthChange = useCallback((value: string) => {
    setSelectedAdSettings((prevSettings) => ({
      ...prevSettings,
      month: value
    }));
  }, []);

  const handleGuaranteedHourChange = useCallback((value: boolean) => {
    setSelectedAdSettings((prevSettings) => ({
      ...prevSettings,
      guaranteed_hour: value
    }));
  }, []);

  const handleThirdPartyChange = useCallback((value: boolean) => {
    setSelectedAdSettings((prevSettings) => ({
      ...prevSettings,
      third_party: value
    }));
  }, []);

  useEffect(() => {
    if (
      selectedAdSettings.audio_duration !== '' ||
      selectedAdSettings.block_position !== '' ||
      selectedAdSettings.month !== '' ||
      selectedAdSettings.guaranteed_hour !== false ||
      selectedAdSettings.third_party !== false
    ) {
      console.log(selectedAdSettings);
    }
  }, [selectedAdSettings]);

  return (
    <div className={clsx(s.adSettings)}>
      <div className={clsx(s.adSettingsSelector)}>
        <div>
          <p>{SELECT_DURATION_LABEL}</p>
          <AdDurationSelector onDurationChange={handleDurationChange} />
        </div>
        <div>
          <p>{SELECT_POSITION_LABEL}</p>
          <AdPositionSelector onPositionChange={handlePositionChange} />
        </div>
        <div>
          <p>{SELECT_MOUNTH_LABEL}</p>
          <AdMonthSelector onMonthChange={handleMonthChange} />
        </div>
      </div>
      <div className={clsx(s.adSettingsSwitch)}>
        <div>
          <p>{SWITCH_GUARANTEED_HOUR_LABEL}</p>
          <Switch
            onChange={handleGuaranteedHourChange}
            checked={selectedAdSettings.guaranteed_hour}
            uncheckedIcon={false}
            checkedIcon={false}
            onColor={onColor}
            activeBoxShadow="none"
          />
        </div>
        <div>
          <p>{SWITCH_THIRD_PARTY_LABEL}</p>
          <Switch
            onChange={handleThirdPartyChange}
            checked={selectedAdSettings.third_party}
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
