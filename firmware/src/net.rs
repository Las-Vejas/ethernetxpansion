use embassy_rp::gpio::{Input, Output};
use embassy_time::Delay;

use embedded_hal_bus::spi::ExclusiveDevice;

use embassy_net_wiznet::{
    chip::W5500,
    Device,
    InitError,
    Runner,
    State,
};

use xpanse_api::bus::spi::{SpiBusHandle, SpiError};

use crate::Ethernet;

pub type EthSpiDevice =
    ExclusiveDevice<SpiBusHandle, Output<'static>, Delay>;

pub type EthRunner<'a> =
    Runner<'a, W5500, EthSpiDevice, Input<'static>, Output<'static>>;

pub type EthDevice<'a> = Device<'a>;


pub const N_RX: usize = 8;
pub const N_TX: usize = 8;

pub type EthState = State<N_RX, N_TX>;


pub const DEFAULT_MAC: [u8; 6] = [0x02, 0x00, 0x00, 0x45, 0x54, 0x48];


/// Resets the W5500 and builds an `embassy-net` device for it.
///
/// The returned `EthRunner` must be driven forever (`runner.run().await`)
/// in its own task, and the `EthDevice` is handed to
/// `embassy_net::new` to get a TCP/IP stack.
pub async fn create_network<'a>(
    eth: Ethernet,
    mac_addr: [u8; 6],
    state: &'a mut EthState,
) -> Result<
    (EthDevice<'a>, EthRunner<'a>),
    InitError<
        embedded_hal_bus::spi::DeviceError<SpiError, core::convert::Infallible>,
    >,
> {
    let spi_device = ExclusiveDevice::new(
        eth.spi,
        eth.cs,
        Delay,
    )
    .expect("Failed to create SPI device for W5500");

    embassy_net_wiznet::new::<N_RX, N_TX, W5500, _, _, _>(
        mac_addr,
        state,
        spi_device,
        eth.int,
        eth.rst,
    )
    .await
}
