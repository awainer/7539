import React, { Component } from 'react';

import { List, ListItem, ListSubHeader } from 'react-toolbox/lib/list';
import FontIcon from 'react-toolbox/lib/font_icon';

import styles from './styles.css';

class RecommendationItems extends Component {

  getListItem (item, selectItem) {
    const itemContent = (
      <div className={styles.itemContent}>
        <div className={styles.contentTitle}>
          <span>{item.name}</span>
          <span>Dirección: {item.address}</span>
        </div>
        <div className={styles.contentBody}>
          <span className={styles.chipText}>Distancia: {(item.distance / 1000).toFixed(2)} km</span>
          <span className={styles.chipText}>Tiempo de espera: {((item.waitTime + item.travelTime) / 60).toFixed(2)} min</span>
        </div>
      </div>
    )

    const getStars = ({ratingValue, maxRating}) => {
      const items = [];

      for (let i = 0; i < ratingValue; i++) {
        items.push(<FontIcon key={i} className={`${styles.ratingStar} ${styles.highlight}`} value='star' />);
      }

      for (let i = ratingValue; i < maxRating; i++) {
        items.push(<FontIcon className={styles.ratingStar} key={i} value='star' />);
      }

      return items;
    }

    const ratingValue = item.ranking > 0 ? Math.ceil(item.ranking) : 0;
    const maxRating = 5;
    const rating = (
      <div className={styles.rating}>
        { getStars({ratingValue, maxRating}) }
      </div>
    );

    return (
      <ListItem
        key={item.id}
        onClick={() => selectItem(item)}
        className={styles.recommendation}
        avatar='https://s3-eu-west-1.amazonaws.com/nusdigital/group/images/99/medium/Red_Cross.png'
        itemContent={itemContent}
        rightIcon={rating}
      />
    );
  }

  render () {
    const { items, selectItem } = this.props;
    return (
      <List
        className={styles.recommendationItems}
        selectable
        ripple
      >
        <ListSubHeader caption='Recomendaciones' />
        {
          (items || []).map(item => this.getListItem(item, selectItem))
        }
      </List>
    )
  }
}

export default RecommendationItems;