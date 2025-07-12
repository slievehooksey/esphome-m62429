#include "esphome/core/log.h"
#include "m62429.h"

namespace esphome {
namespace m62429 {

static const char *TAG = "M62429.output";

void m62429Controller::setup() {
  uint8_t clk = clk_pin_->get_pin();
  uint8_t dio = dio_pin_->get_pin();

  volume_controller_ = make_unique<M62429>();
  volume_controller_->begin(dio, clk);
}

void m62429Controller::set_level(uint8_t volume, uint8_t channel) {
  ESP_LOGD(TAG, "Setting Channel %d Volume to %d", channel, volume);
  volume_controller_->setVolume(channel, volume);
}

void m62429Controller::increase(uint8_t channel) {
  ESP_LOGD(TAG, "Increasing Channel %d", channel);
  volume_controller_->incr(channel);
}

void m62429Controller::decrease(uint8_t channel) {
  ESP_LOGD(TAG, "Decreasing Channel %d", channel);
  volume_controller_->decr(channel);
}

void m62429Controller::mute() {
  ESP_LOGD(TAG, "Muting");
  volume_controller_->muteOn();
}

void m62429Controller::unmute() {
  ESP_LOGD(TAG, "Unmuting");
  volume_controller_->muteOff();
}

void m62429Controller::toggle_mute() {
  ESP_LOGD(TAG, "Toggling Mute");
  if (volume_controller_->isMuted()) {
    volume_controller_->muteOff();
  } else {
    volume_controller_->muteOn();
  }
}

void m62429Controller::dump_config() { ESP_LOGCONFIG(TAG, "Empty float output"); }

}  // namespace m62429
}  // namespace esphome
